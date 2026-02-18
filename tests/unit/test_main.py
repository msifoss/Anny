from unittest.mock import patch


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("healthy", "degraded")
    assert "checks" in data
    assert "config" in data["checks"]
    assert "credentials" in data["checks"]
    assert "memory" in data["checks"]


@patch("anny.main.settings")
def test_health_check_degraded_when_config_missing(mock_settings, client):
    """Health reports degraded when required config is empty."""
    mock_settings.google_service_account_key_path = ""
    mock_settings.ga4_property_id = ""
    mock_settings.search_console_site_url = ""
    mock_settings.memory_store_path = "~/.anny/memory.json"
    response = client.get("/health")
    data = response.json()
    assert data["checks"]["config"] is False
    assert data["status"] == "degraded"
