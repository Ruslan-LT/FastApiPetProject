from fastapi import APIRouter, Request, Depends, HTTPException, status, Response, Path
from typing import Annotated

from admin.dependencies import admin_check, get_admin_service
from admin.service import AdminService

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/read_post", dependencies=[Depends(admin_check)])
async def read_post(post_id: int | None = None,
                      request: Request = None,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.read_post(request,post_id)

@admin_router.post("/accept", dependencies=[Depends(admin_check)])
async def accept_post(post_id: int | None = None,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.accept_post(post_id,)


@admin_router.post("/decline", dependencies=[Depends(admin_check)])
async def decline_post(post_id: int | None = None,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.decline_post(post_id,)


@admin_router.delete("/delete", dependencies=[Depends(admin_check)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.delete_post(post_id)

