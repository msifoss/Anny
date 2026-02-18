from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from anny.clients.tag_manager import TagManagerClient
from anny.core.dependencies import get_tag_manager_client, verify_api_key
from anny.main import app


def _mock_gtm_client():
    return MagicMock(spec=TagManagerClient)


def _setup_overrides(mock_client):
    app.dependency_overrides[get_tag_manager_client] = lambda: mock_client
    app.dependency_overrides[verify_api_key] = lambda: None


def _teardown_overrides():
    app.dependency_overrides.pop(get_tag_manager_client, None)
    app.dependency_overrides.pop(verify_api_key, None)


def test_accounts_endpoint():
    mock_client = _mock_gtm_client()
    _setup_overrides(mock_client)
    mock_client.list_accounts.return_value = [{"accountId": "123", "name": "Test"}]

    tc = TestClient(app)
    response = tc.get("/api/tag-manager/accounts")

    _teardown_overrides()

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1


def test_containers_endpoint():
    mock_client = _mock_gtm_client()
    _setup_overrides(mock_client)
    mock_client.list_containers.return_value = [{"containerId": "456", "name": "Web"}]

    tc = TestClient(app)
    response = tc.get("/api/tag-manager/containers?account_id=123")

    _teardown_overrides()

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_tags_endpoint():
    mock_client = _mock_gtm_client()
    _setup_overrides(mock_client)
    mock_client.list_tags.return_value = [{"tagId": "1", "name": "GA4"}]

    tc = TestClient(app)
    response = tc.get("/api/tag-manager/tags?container_path=accounts/123/containers/456")

    _teardown_overrides()

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_triggers_endpoint():
    mock_client = _mock_gtm_client()
    _setup_overrides(mock_client)
    mock_client.list_triggers.return_value = [{"triggerId": "1", "name": "All Pages"}]

    tc = TestClient(app)
    response = tc.get("/api/tag-manager/triggers?container_path=accounts/123/containers/456")

    _teardown_overrides()

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_variables_endpoint():
    mock_client = _mock_gtm_client()
    _setup_overrides(mock_client)
    mock_client.list_variables.return_value = [{"variableId": "1", "name": "URL"}]

    tc = TestClient(app)
    response = tc.get("/api/tag-manager/variables?container_path=accounts/123/containers/456")

    _teardown_overrides()

    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_container_setup_endpoint():
    mock_client = _mock_gtm_client()
    _setup_overrides(mock_client)
    mock_client.list_tags.return_value = [{"tagId": "1", "name": "GA4"}]
    mock_client.list_triggers.return_value = []
    mock_client.list_variables.return_value = []

    tc = TestClient(app)
    response = tc.get("/api/tag-manager/container-setup?container_path=accounts/123/containers/456")

    _teardown_overrides()

    assert response.status_code == 200
    data = response.json()
    assert data["tag_count"] == 1
    assert data["trigger_count"] == 0
    assert data["variable_count"] == 0
