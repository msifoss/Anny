"""Tests for MCP HTTP Bearer token authentication."""

from unittest.mock import patch

from anny.core.dependencies import verify_mcp_bearer_token

TEST_API_KEY = "test-secret-key-12345"


class TestMCPBearerValidation:
    """Test verify_mcp_bearer_token used by DebugTokenVerifier."""

    @patch("anny.core.dependencies.settings")
    def test_valid_token_returns_true(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        assert verify_mcp_bearer_token(TEST_API_KEY) is True

    @patch("anny.core.dependencies.settings")
    def test_invalid_token_returns_false(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        assert verify_mcp_bearer_token("wrong-key") is False

    @patch("anny.core.dependencies.settings")
    def test_empty_token_returns_false(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        assert verify_mcp_bearer_token("") is False

    @patch("anny.core.dependencies.settings")
    def test_auth_disabled_when_no_key(self, mock_settings):
        mock_settings.anny_api_key = ""
        assert verify_mcp_bearer_token("any-token") is True

    @patch("anny.core.dependencies.settings")
    def test_auth_disabled_accepts_empty_token(self, mock_settings):
        mock_settings.anny_api_key = ""
        assert verify_mcp_bearer_token("") is True
