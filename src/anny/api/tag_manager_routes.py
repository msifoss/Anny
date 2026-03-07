from fastapi import APIRouter, Depends, Query, Security

from anny.api.models import GTMContainerSetupResponse, GTMListResponse
from anny.clients.tag_manager import TagManagerClient
from anny.core.dependencies import get_tag_manager_client, verify_api_key
from anny.core.services import tag_manager_service

router = APIRouter(prefix="/api/tag-manager", tags=["Tag Manager"])


@router.get("/accounts", response_model=GTMListResponse)
async def accounts(
    client: TagManagerClient = Depends(get_tag_manager_client),
    _: str = Security(verify_api_key),
):
    items = tag_manager_service.get_accounts(client)
    return GTMListResponse(items=items, count=len(items))


@router.get("/containers", response_model=GTMListResponse)
async def containers(
    account_id: str = Query(max_length=50),
    client: TagManagerClient = Depends(get_tag_manager_client),
    _: str = Security(verify_api_key),
):
    items = tag_manager_service.get_containers(client, account_id)
    return GTMListResponse(items=items, count=len(items))


@router.get("/tags", response_model=GTMListResponse)
async def tags(
    container_path: str = Query(max_length=200),
    client: TagManagerClient = Depends(get_tag_manager_client),
    _: str = Security(verify_api_key),
):
    items = tag_manager_service.get_tags(client, container_path)
    return GTMListResponse(items=items, count=len(items))


@router.get("/triggers", response_model=GTMListResponse)
async def triggers(
    container_path: str = Query(max_length=200),
    client: TagManagerClient = Depends(get_tag_manager_client),
    _: str = Security(verify_api_key),
):
    items = tag_manager_service.get_triggers(client, container_path)
    return GTMListResponse(items=items, count=len(items))


@router.get("/variables", response_model=GTMListResponse)
async def variables(
    container_path: str = Query(max_length=200),
    client: TagManagerClient = Depends(get_tag_manager_client),
    _: str = Security(verify_api_key),
):
    items = tag_manager_service.get_variables(client, container_path)
    return GTMListResponse(items=items, count=len(items))


@router.get("/container-setup", response_model=GTMContainerSetupResponse)
async def container_setup(
    container_path: str = Query(max_length=200),
    client: TagManagerClient = Depends(get_tag_manager_client),
    _: str = Security(verify_api_key),
):
    return tag_manager_service.get_container_setup(client, container_path)
