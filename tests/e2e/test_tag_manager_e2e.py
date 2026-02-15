import pytest


@pytest.mark.e2e
class TestGTMAccounts:
    def test_returns_200(self, live_client):
        resp = live_client.get("/api/tag-manager/accounts")
        assert resp.status_code == 200

    def test_response_shape(self, live_client):
        resp = live_client.get("/api/tag-manager/accounts")
        data = resp.json()
        assert "items" in data
        assert "count" in data
        assert isinstance(data["items"], list)
        assert data["count"] == len(data["items"])

    def test_account_shape(self, live_client):
        resp = live_client.get("/api/tag-manager/accounts")
        data = resp.json()
        if not data["items"]:
            pytest.skip("No GTM accounts available")
        account = data["items"][0]
        assert isinstance(account, dict)


@pytest.mark.e2e
class TestGTMContainers:
    def _get_first_account_id(self, live_client):
        resp = live_client.get("/api/tag-manager/accounts")
        data = resp.json()
        if not data["items"]:
            pytest.skip("No GTM accounts available")
        account = data["items"][0]
        # Account path is like "accounts/123456"
        path = account.get("path", "")
        if not path:
            pytest.skip("Account has no path field")
        return path.split("/")[-1]

    def test_returns_200(self, live_client):
        account_id = self._get_first_account_id(live_client)
        resp = live_client.get("/api/tag-manager/containers", params={"account_id": account_id})
        assert resp.status_code == 200

    def test_response_shape(self, live_client):
        account_id = self._get_first_account_id(live_client)
        resp = live_client.get("/api/tag-manager/containers", params={"account_id": account_id})
        data = resp.json()
        assert "items" in data
        assert "count" in data
        assert isinstance(data["items"], list)
