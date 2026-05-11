from fastapi import APIRouter, Request, Depends, HTTPException, status, Response, Path
from typing import Annotated
from users.dependencies import check_user_have_access_token
from admin.dependencies import admin_check, get_admin_service
from admin.service import AdminService
from auth.tokens_check_dependencies import jwt_access_token_check_dependency,jwt_refresh_token_check_dependency

admin_router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(admin_check), Depends(check_user_have_access_token),
                                              Depends(jwt_refresh_token_check_dependency),Depends(jwt_access_token_check_dependency)])

@admin_router.get("/read_post", )
async def read_post(post_id: int | None = None,
                      request: Request = None,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.read_post(request,post_id)

@admin_router.post("/accept",)
async def accept_post(post_id: int | None = None,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.accept_post(post_id,)


@admin_router.post("/decline",)
async def decline_post(post_id: int | None = None,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.decline_post(post_id,)


@admin_router.delete("/delete",
                     status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int,
                      admin_service: AdminService = Depends(get_admin_service)):
    return await admin_service.delete_post(post_id)

