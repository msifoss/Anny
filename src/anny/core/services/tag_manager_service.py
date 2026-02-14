from anny.clients.tag_manager import TagManagerClient


def get_accounts(client: TagManagerClient) -> list[dict]:
    """List all GTM accounts."""
    return client.list_accounts()


def get_containers(client: TagManagerClient, account_id: str) -> list[dict]:
    """List containers for a GTM account."""
    return client.list_containers(account_id)


def get_container_setup(client: TagManagerClient, container_path: str) -> dict:
    """Get a summary of a container's tags, triggers, and variables."""
    tags = client.list_tags(container_path)
    triggers = client.list_triggers(container_path)
    variables = client.list_variables(container_path)

    return {
        "tags": tags,
        "tag_count": len(tags),
        "triggers": triggers,
        "trigger_count": len(triggers),
        "variables": variables,
        "variable_count": len(variables),
    }
