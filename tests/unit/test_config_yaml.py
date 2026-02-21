"""Tests for config.yaml loading and Settings integration."""

import os
import subprocess
import sys

import yaml

from anny.core.config import Settings, _flatten_yaml, _load_yaml_config

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")
CONFIG_GET = os.path.join(PROJECT_ROOT, "scripts", "config-get")


class TestConfigYamlFile:
    """Tests that config.yaml exists and parses correctly."""

    def test_config_yaml_exists(self):
        assert os.path.isfile(CONFIG_PATH), "config.yaml should exist at project root"

    def test_config_yaml_parses(self):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)
        assert "app" in data
        assert "deploy" in data

    def test_config_yaml_has_expected_sections(self):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for section in ("app", "deploy", "infra", "backup", "monitoring"):
            assert section in data, f"config.yaml should have '{section}' section"

    def test_config_yaml_app_version(self):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data["app"]["version"] == "0.8.0"


class TestFlattenYaml:
    """Tests for the _flatten_yaml helper."""

    def test_simple_flatten(self):
        result = _flatten_yaml({"app": {"version": "1.0", "port": 8000}})
        assert result == {"app_version": "1.0", "app_port": 8000}

    def test_deeply_nested(self):
        result = _flatten_yaml({"a": {"b": {"c": "deep"}}})
        assert result == {"a_b_c": "deep"}

    def test_flat_input(self):
        result = _flatten_yaml({"key": "value"})
        assert result == {"key": "value"}

    def test_empty_dict(self):
        result = _flatten_yaml({})
        assert not result

    def test_mixed_nesting(self):
        result = _flatten_yaml({"top": "val", "nested": {"inner": 42}})
        assert result == {"top": "val", "nested_inner": 42}


class TestLoadYamlConfig:
    """Tests for _load_yaml_config."""

    def test_returns_flattened_dict(self):
        result = _load_yaml_config()
        assert isinstance(result, dict)
        assert "app_version" in result
        assert "deploy_domain" in result

    def test_values_match_config_file(self):
        result = _load_yaml_config()
        assert result["app_version"] == "0.8.0"
        assert result["deploy_domain"] == "anny.membies.com"
        assert result["backup_retention_days"] == 7


class TestSettingsYamlIntegration:
    """Tests that Settings picks up config.yaml values with correct precedence."""

    def test_settings_loads_yaml_defaults(self):
        s = Settings(
            _env_file=None,
            google_service_account_key_path="",
            anny_api_key="",
            sentry_dsn="",
        )
        assert s.app_version == "0.8.0"
        assert s.deploy_domain == "anny.membies.com"
        assert s.backup_retention_days == 7

    def test_env_var_overrides_yaml(self, monkeypatch):
        monkeypatch.setenv("APP_VERSION", "9.9.9")
        s = Settings(
            _env_file=None,
            google_service_account_key_path="",
            anny_api_key="",
            sentry_dsn="",
        )
        assert s.app_version == "9.9.9"

    def test_kwargs_override_yaml(self):
        s = Settings(
            _env_file=None,
            app_version="override",
            google_service_account_key_path="",
            anny_api_key="",
            sentry_dsn="",
        )
        assert s.app_version == "override"

    def test_missing_config_yaml_uses_code_defaults(self, monkeypatch, tmp_path):
        # Point config loader away from real config.yaml
        monkeypatch.chdir(tmp_path)
        # Settings should still work with code defaults
        s = Settings(
            _env_file=None,
            google_service_account_key_path="",
            anny_api_key="",
            sentry_dsn="",
        )
        assert s.app_version == "0.8.0"  # code default matches yaml, but this proves no crash

    def test_deploy_fields_loaded(self):
        s = Settings(
            _env_file=None,
            google_service_account_key_path="",
            anny_api_key="",
            sentry_dsn="",
        )
        assert s.deploy_remote_dir == "/opt/anny"
        assert s.deploy_ssh_key == "~/.ssh/webengine_deploy"
        assert s.deploy_health_check_timeout == 60


class TestConfigGetScript:
    """Tests for the config-get CLI helper."""

    def test_reads_deploy_domain(self):
        result = subprocess.run(
            [sys.executable, CONFIG_GET, "deploy.domain"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "anny.membies.com"

    def test_reads_backup_retention_days(self):
        result = subprocess.run(
            [sys.executable, CONFIG_GET, "backup.retention_days"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "7"

    def test_reads_app_version(self):
        result = subprocess.run(
            [sys.executable, CONFIG_GET, "app.version"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "0.8.0"

    def test_invalid_key_exits_nonzero(self):
        result = subprocess.run(
            [sys.executable, CONFIG_GET, "nonexistent.key"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
        )
        assert result.returncode != 0

    def test_no_args_exits_nonzero(self):
        result = subprocess.run(
            [sys.executable, CONFIG_GET],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
        )
        assert result.returncode != 0
