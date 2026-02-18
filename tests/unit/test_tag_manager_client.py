from unittest.mock import MagicMock

import pytest
from googleapiclient.errors import HttpError
from httplib2 import Response

from anny.clients.tag_manager import TagManagerClient
from anny.core.exceptions import APIError


def test_list_accounts():
    service = MagicMock()
    service.accounts().list().execute.return_value = {
        "account": [
            {"accountId": "123", "name": "My Account", "path": "accounts/123"},
        ]
    }
    client = TagManagerClient(service)
    accounts = client.list_accounts()

    assert len(accounts) == 1
    assert accounts[0]["accountId"] == "123"
    assert accounts[0]["name"] == "My Account"


def test_list_accounts_empty():
    service = MagicMock()
    service.accounts().list().execute.return_value = {"account": []}
    client = TagManagerClient(service)
    assert client.list_accounts() == []


def test_list_accounts_api_failure():
    service = MagicMock()
    service.accounts().list().execute.side_effect = HttpError(
        Response({"status": "500"}), b"internal error"
    )
    client = TagManagerClient(service)

    with pytest.raises(APIError, match="GTM list accounts failed"):
        client.list_accounts()


def test_list_containers():
    service = MagicMock()
    service.accounts().containers().list().execute.return_value = {
        "container": [
            {
                "containerId": "456",
                "name": "Web",
                "publicId": "GTM-XXXX",
                "path": "accounts/123/containers/456",
            }
        ]
    }
    client = TagManagerClient(service)
    containers = client.list_containers("123")

    assert len(containers) == 1
    assert containers[0]["containerId"] == "456"
    assert containers[0]["publicId"] == "GTM-XXXX"


def test_list_tags():
    service = MagicMock()
    service.accounts().containers().workspaces().tags().list().execute.return_value = {
        "tag": [
            {"tagId": "1", "name": "GA4 Config", "type": "gaawc"},
            {"tagId": "2", "name": "Conversion", "type": "awct"},
        ]
    }
    client = TagManagerClient(service)
    tags = client.list_tags("accounts/123/containers/456")

    assert len(tags) == 2
    assert tags[0]["name"] == "GA4 Config"


def test_list_triggers():
    service = MagicMock()
    service.accounts().containers().workspaces().triggers().list().execute.return_value = {
        "trigger": [
            {"triggerId": "1", "name": "All Pages", "type": "pageview"},
        ]
    }
    client = TagManagerClient(service)
    triggers = client.list_triggers("accounts/123/containers/456")

    assert len(triggers) == 1
    assert triggers[0]["name"] == "All Pages"


def test_list_variables():
    service = MagicMock()
    service.accounts().containers().workspaces().variables().list().execute.return_value = {
        "variable": [
            {"variableId": "1", "name": "Page URL", "type": "u"},
        ]
    }
    client = TagManagerClient(service)
    variables = client.list_variables("accounts/123/containers/456")

    assert len(variables) == 1
    assert variables[0]["name"] == "Page URL"


def test_ensure_workspace_path_appends_default():
    # pylint: disable=protected-access
    assert (
        TagManagerClient._ensure_workspace_path("accounts/123/containers/456")
        == "accounts/123/containers/456/workspaces/default"
    )


def test_ensure_workspace_path_preserves_existing():
    # pylint: disable=protected-access
    path = "accounts/123/containers/456/workspaces/5"
    assert TagManagerClient._ensure_workspace_path(path) == path
