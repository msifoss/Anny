from googleapiclient.discovery import Resource

from anny.core.exceptions import APIError


class TagManagerClient:
    """Wraps the Google Tag Manager API v2."""

    def __init__(self, service: Resource):
        self._service = service

    def list_accounts(self) -> list[dict]:
        """List all GTM accounts accessible by the service account."""
        try:
            response = self._service.accounts().list().execute()
        except Exception as exc:
            raise APIError(f"GTM list accounts failed: {exc}", service="tag_manager") from exc

        return [
            {
                "accountId": a.get("accountId", ""),
                "name": a.get("name", ""),
                "path": a.get("path", ""),
            }
            for a in response.get("account", [])
        ]

    def list_containers(self, account_id: str) -> list[dict]:
        """List containers for a given account."""
        parent = f"accounts/{account_id.removeprefix('accounts/')}"
        try:
            response = self._service.accounts().containers().list(parent=parent).execute()
        except Exception as exc:
            raise APIError(f"GTM list containers failed: {exc}", service="tag_manager") from exc

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
        except Exception as exc:
            raise APIError(f"GTM list tags failed: {exc}", service="tag_manager") from exc

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
        except Exception as exc:
            raise APIError(f"GTM list triggers failed: {exc}", service="tag_manager") from exc

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
        except Exception as exc:
            raise APIError(f"GTM list variables failed: {exc}", service="tag_manager") from exc

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
