from unittest.mock import MagicMock

from anny.core.services import tag_manager_service


def test_get_accounts():
    mock_client = MagicMock()
    mock_client.list_accounts.return_value = [{"accountId": "123", "name": "Test"}]

    result = tag_manager_service.get_accounts(mock_client)

    assert len(result) == 1
    mock_client.list_accounts.assert_called_once()


def test_get_containers():
    mock_client = MagicMock()
    mock_client.list_containers.return_value = [{"containerId": "456", "name": "Web"}]

    result = tag_manager_service.get_containers(mock_client, "123")

    assert len(result) == 1
    mock_client.list_containers.assert_called_once_with("123")


def test_get_container_setup():
    mock_client = MagicMock()
    mock_client.list_tags.return_value = [{"tagId": "1", "name": "GA4"}]
    mock_client.list_triggers.return_value = [{"triggerId": "1", "name": "All Pages"}]
    mock_client.list_variables.return_value = [
        {"variableId": "1", "name": "URL"},
        {"variableId": "2", "name": "Click"},
    ]

    result = tag_manager_service.get_container_setup(mock_client, "accounts/123/containers/456")

    assert result["tag_count"] == 1
    assert result["trigger_count"] == 1
    assert result["variable_count"] == 2
    assert len(result["tags"]) == 1
    assert len(result["triggers"]) == 1
    assert len(result["variables"]) == 2
