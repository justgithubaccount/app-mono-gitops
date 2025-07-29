import logging
import os
from opentelemetry import trace, logs
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

def setup_tracing(app) -> None:
    """
    Настройка OpenTelemetry для traces и logs согласно CNCF практикам.
    """
    # Resource с метаданными сервиса и Kubernetes
    resource = Resource(attributes={
        "service.name": os.getenv("OTEL_SERVICE_NAME", "chat-api"),
        "service.version": os.getenv("APP_VERSION", "0.1.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
        # Kubernetes metadata - обязательные атрибуты для observability
        "k8s.pod.name": os.getenv("K8S_POD_NAME", "unknown"),
        "k8s.namespace": os.getenv("K8S_NAMESPACE", "chat"),
        "k8s.node.name": os.getenv("K8S_NODE_NAME", "unknown"),
        "k8s.deployment.name": os.getenv("K8S_DEPLOYMENT_NAME", "chat-api"),
        # Дополнительные метаданные для трассировки
        "k8s.container.name": os.getenv("K8S_CONTAINER_NAME", "chat-api"),
        "k8s.pod.uid": os.getenv("K8S_POD_UID", "unknown"),
    })
    
    # OTLP endpoint согласно OpenTelemetry specification
    # В production используем service mesh или sidecar pattern
    otlp_endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://vector-gateway.observability.svc.cluster.local:4318"
    )
    
    # Добавляем /v1/traces к endpoint если не указан полный путь
    traces_endpoint = f"{otlp_endpoint}/v1/traces" if not otlp_endpoint.endswith("/v1/traces") else otlp_endpoint
    logs_endpoint = f"{otlp_endpoint}/v1/logs" if not otlp_endpoint.endswith("/v1/logs") else otlp_endpoint
    
    # === TRACES ===
    provider = TracerProvider(resource=resource)
    
    # Создаем exporter без параметра insecure
    # Безопасность определяется через протокол в URL (http vs https)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=traces_endpoint,
        # headers можно использовать для auth если нужно
        headers={"X-Scope-OrgID": os.getenv("GRAFANA_TENANT_ID", "1")} if os.getenv("GRAFANA_TENANT_ID") else None
    )
    
    # BatchSpanProcessor для оптимальной производительности
    trace_processor = BatchSpanProcessor(
        otlp_trace_exporter,
        # Настройки батчинга согласно CNCF рекомендациям
        max_queue_size=2048,
        max_export_batch_size=512,
        schedule_delay_millis=5000,
    )
    provider.add_span_processor(trace_processor)
    trace.set_tracer_provider(provider)
    
    # === LOGS ===
    log_provider = LoggerProvider(resource=resource)
    
    otlp_log_exporter = OTLPLogExporter(
        endpoint=logs_endpoint,
        headers={"X-Scope-OrgID": os.getenv("GRAFANA_TENANT_ID", "1")} if os.getenv("GRAFANA_TENANT_ID") else None
    )
    
    log_processor = BatchLogRecordProcessor(
        otlp_log_exporter,
        max_queue_size=2048,
        max_export_batch_size=512,
        schedule_delay_millis=5000,
    )
    log_provider.add_log_record_processor(log_processor)
    logs.set_logger_provider(log_provider)
    
    # Подключаем OpenTelemetry handler к root logger
    handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=log_provider
    )
    
    # Получаем root logger и добавляем handler
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
    # Устанавливаем формат для консольного вывода
    # В production используем JSON формат для парсинга
    if os.getenv("ENVIRONMENT") == "production":
        # JSON logging для production
        import json
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_obj = {
                    "timestamp": self.formatTime(record),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": record.getMessage(),
                    "pathname": record.pathname,
                    "lineno": record.lineno,
                }
                # Добавляем trace context если есть
                span = trace.get_current_span()
                if span.is_recording():
                    ctx = span.get_span_context()
                    log_obj["trace_id"] = format(ctx.trace_id, '032x')
                    log_obj["span_id"] = format(ctx.span_id, '016x')
                return json.dumps(log_obj)
        
        json_handler = logging.StreamHandler()
        json_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(json_handler)
    else:
        # Человекочитаемый формат для dev окружения
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s',
            force=True
        )
    
    # FastAPI instrumentation с дополнительными атрибутами
    FastAPIInstrumentor().instrument_app(
        app, 
        tracer_provider=provider,
        # Добавляем кастомные атрибуты к спанам
        server_request_hook=lambda span, scope: span.set_attributes({
            "http.url.path": scope.get("path"),
            "http.url.query": scope.get("query_string", b"").decode(),
            "asgi.event_type": scope.get("type"),
        })
    )
    
    # Логируем успешную инициализацию
    logger = logging.getLogger(__name__)
    logger.info(
        "OpenTelemetry initialized",
        extra={
            "otlp_endpoint": otlp_endpoint,
            "service_name": resource.attributes.get("service.name"),
            "environment": resource.attributes.get("deployment.environment"),
        }
    )