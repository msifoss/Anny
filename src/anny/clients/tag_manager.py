import logging
import re

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from anny.core.exceptions import APIError

logger = logging.getLogger("anny")


class TagManagerClient:
    """Wraps the Google Tag Manager API v2."""

    def __init__(self, service: Resource):
        self._service = service

    def list_accounts(self) -> list[dict]:
        """List all GTM accounts accessible by the service account."""
        try:
            response = self._service.accounts().list().execute()
        except HttpError as exc:
            logger.warning("GTM list accounts failed: %s %s", exc.status_code, exc.reason)
            raise APIError(
                "GTM list accounts failed",
                service="tag_manager",
            ) from exc

        return [
            {
                "accountId": a.get("accountId", ""),
                "name": a.get("name", ""),
                "path": a.get("path", ""),
            }
            for a in response.get("account", [])
        ]

    @staticmethod
    def _validate_account_id(account_id: str) -> None:
        """Validate account_id contains only digits."""
        raw = account_id.removeprefix("accounts/")
        if not re.fullmatch(r"\d+", raw):
            raise APIError("Invalid account ID format", service="tag_manager")

    @staticmethod
    def _validate_container_path(container_path: str) -> None:
        """Validate container_path matches expected GTM path format."""
        if not re.fullmatch(r"accounts/\d+/containers/\d+(/workspaces/\w+)?", container_path):
            raise APIError("Invalid container path format", service="tag_manager")

    def list_containers(self, account_id: str) -> list[dict]:
        """List containers for a given account."""
        self._validate_account_id(account_id)
        parent = f"accounts/{account_id.removeprefix('accounts/')}"
        try:
            response = self._service.accounts().containers().list(parent=parent).execute()
        except HttpError as exc:
            logger.warning("GTM list containers failed: %s %s", exc.status_code, exc.reason)
            raise APIError(
                "GTM list containers failed",
                service="tag_manager",
            ) from exc

        return [
            {
                "containerId": c.get("containerId", ""),
                "name": c.get("name", ""),
                "publicId": c.get("publicId", ""),
                "path": c.get("path", ""),
            }
            for c in response.get("container", [])
        ]

    def list_tags(self, container_path: str) -> list[dict]:
        """List tags in a container workspace."""
        self._validate_container_path(container_path)
        workspace_path = self._ensure_workspace_path(container_path)
        try:
            response = (
                self._service.accounts()
                .containers()
                .workspaces()
                .tags()
                .list(parent=workspace_path)
                .execute()
            )
        except HttpError as exc:
            logger.warning("GTM list tags failed: %s %s", exc.status_code, exc.reason)
            raise APIError(
                "GTM list tags failed",
                service="tag_manager",
            ) from exc

        return [
            {
                "tagId": t.get("tagId", ""),
                "name": t.get("name", ""),
                "type": t.get("type", ""),
            }
            for t in response.get("tag", [])
        ]

    def list_triggers(self, container_path: str) -> list[dict]:
        """List triggers in a container workspace."""
        self._validate_container_path(container_path)
        workspace_path = self._ensure_workspace_path(container_path)
        try:
            response = (
                self._service.accounts()
                .containers()
                .workspaces()
                .triggers()
                .list(parent=workspace_path)
                .execute()
            )
        except HttpError as exc:
            logger.warning("GTM list triggers failed: %s %s", exc.status_code, exc.reason)
            raise APIError(
                "GTM list triggers failed",
                service="tag_manager",
            ) from exc

        return [
            {
                "triggerId": t.get("triggerId", ""),
                "name": t.get("name", ""),
                "type": t.get("type", ""),
            }
            for t in response.get("trigger", [])
        ]

    def list_variables(self, container_path: str) -> list[dict]:
        """List variables in a container workspace."""
        self._validate_container_path(container_path)
        workspace_path = self._ensure_workspace_path(container_path)
        try:
            response = (
                self._service.accounts()
                .containers()
                .workspaces()
                .variables()
                .list(parent=workspace_path)
                .execute()
            )
        except HttpError as exc:
            logger.warning("GTM list variables failed: %s %s", exc.status_code, exc.reason)
            raise APIError(
                "GTM list variables failed",
                service="tag_manager",
            ) from exc

        return [
            {
                "variableId": v.get("variableId", ""),
                "name": v.get("name", ""),
                "type": v.get("type", ""),
            }
            for v in response.get("variable", [])
        ]

    @staticmethod
    def _ensure_workspace_path(container_path: str) -> str:
        """If container_path doesn't include a workspace, append /workspaces/default."""
        if "/workspaces/" not in container_path:
            return f"{container_path}/workspaces/default"
        return container_path
