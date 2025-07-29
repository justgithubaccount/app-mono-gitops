# apps/chat/app/observability/tracing.py
import logging
import os

from opentelemetry import trace
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
    Настройка OpenTelemetry для traces и logs.
    """
    # Resource с метаданными сервиса и Kubernetes
    resource = Resource(attributes={
        "service.name": "chat-api",
        "service.version": os.getenv("APP_VERSION", "0.1.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
        # Kubernetes metadata
        "k8s.pod.name": os.getenv("K8S_POD_NAME", "unknown"),
        "k8s.namespace": os.getenv("K8S_NAMESPACE", "chat"),
        "k8s.node.name": os.getenv("K8S_NODE_NAME", "unknown"),
    })
    
    # Endpoint для Vector Gateway в Kubernetes
    otlp_endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://vector-gateway.observability.svc.cluster.local:4318"
    )
    
    # === TRACES ===
    provider = TracerProvider(resource=resource)
    
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=otlp_endpoint,
        # insecure=True,  # В production использовать TLS
    )
    
    trace_processor = BatchSpanProcessor(otlp_trace_exporter)
    provider.add_span_processor(trace_processor)
    trace.set_tracer_provider(provider)
    
    # === LOGS ===
    log_provider = LoggerProvider(resource=resource)
    
    otlp_log_exporter = OTLPLogExporter(
        endpoint=otlp_endpoint,
        insecure=True,
    )
    
    log_processor = BatchLogRecordProcessor(otlp_log_exporter)
    log_provider.add_log_record_processor(log_processor)
    logs.set_logger_provider(log_provider)
    
    # Подключаем OpenTelemetry handler к root logger
    handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=log_provider
    )
    logging.getLogger().addHandler(handler)
    
    # Устанавливаем формат для консольного вывода (для дебага)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # FastAPI instrumentation
    FastAPIInstrumentor().instrument_app(app, tracer_provider=provider)