from fastapi.testclient import TestClient

from app.main import create_app


def test_logging_enriched(capfd):
    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/projects")
    assert response.status_code == 200

    out, _ = capfd.readouterr()
    # logs are JSON per line
    assert '"event": "project_list_requested"' in out
    assert '"trace_id":' in out
