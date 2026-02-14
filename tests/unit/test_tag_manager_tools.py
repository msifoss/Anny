from unittest.mock import MagicMock

from anny.core.formatting import format_table
from anny.core.services import tag_manager_service


def test_gtm_list_accounts_tool_flow():
    mock_client = MagicMock()
    mock_client.list_accounts.return_value = [
        {"accountId": "123", "name": "My Account", "path": "accounts/123"}
    ]
    rows = tag_manager_service.get_accounts(mock_client)
    result = format_table(rows)

    assert "My Account" in result
    assert "123" in result


def test_gtm_list_containers_tool_flow():
    mock_client = MagicMock()
    mock_client.list_containers.return_value = [
        {
            "containerId": "456",
            "name": "Web",
            "publicId": "GTM-XXXX",
            "path": "accounts/123/containers/456",
        }
    ]
    rows = tag_manager_service.get_containers(mock_client, "123")
    result = format_table(rows)

    assert "Web" in result
    assert "GTM-XXXX" in result


def test_gtm_container_setup_tool_flow():
    mock_client = MagicMock()
    mock_client.list_tags.return_value = [{"tagId": "1", "name": "GA4", "type": "gaawc"}]
    mock_client.list_triggers.return_value = [
        {"triggerId": "1", "name": "All Pages", "type": "pageview"}
    ]
    mock_client.list_variables.return_value = []

    setup = tag_manager_service.get_container_setup(mock_client, "accounts/123/containers/456")

    assert setup["tag_count"] == 1
    assert setup["trigger_count"] == 1
    assert setup["variable_count"] == 0


def test_gtm_list_tags_tool_flow():
    mock_client = MagicMock()
    mock_client.list_tags.return_value = [{"tagId": "1", "name": "GA4 Config", "type": "gaawc"}]
    rows = mock_client.list_tags("accounts/123/containers/456")
    result = format_table(rows)

    assert "GA4 Config" in result
