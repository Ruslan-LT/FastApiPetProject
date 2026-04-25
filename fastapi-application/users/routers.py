from typing import Annotated, Any
from fastapi import (Depends, APIRouter, Response, Request, HTTPException, status, Path)
from users.schemas import UserInDB, UserCreate, UserRead, UserUpdate
from users.security import security, get_password_hash, verify_password,\
                            get_auth_username,COOKIE_SESSION_ID_KEY,generate_session_id, get_session_id
from users.service import UserService
from users.dependencies import get_user_service
from news.schemas import PostRead, PostUpdate

user_router = APIRouter(tags=["users"],
                        prefix="/users",)

@user_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, response: Response, request: Request, user_service:UserService=Depends(get_user_service)):
    return await user_service.create_user_account(user,response,request)

@user_router.post("/login")
async def user_login(response: Response, auth_user:Annotated[UserRead, Depends(get_auth_username)],
                     user_service:UserService=Depends(get_user_service)):
    return await user_service.login_user_account(auth_user,response)

@user_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def user_logout(response: Response,
                      request: Request,
                      user_service:UserService=Depends(get_user_service)):
    return await user_service.logout_user_account(response, request)

@user_router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_current_user(request: Request,
                           user_service:UserService=Depends(get_user_service),
                           session_id:str=Depends(get_session_id)):
    return await user_service.read_auth_user_account(request, session_id)

@user_router.put("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_user_account_data(user_update:UserUpdate,
                                   user_service:UserService=Depends(get_user_service),
                                   session_id:str=Depends(get_session_id)):

    return await user_service.update_user_account(user_update, session_id)

@user_router.delete("/my_post",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_user(post_id: int,
                              request: Request,
                              user_service:UserService=Depends(get_user_service)):

     await user_service.delete_post_by_user(request,post_id)

@user_router.put("/my_post/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def update_user_post(post_id:Annotated[int,Path()],
                           request:Request,
                           post_update: PostUpdate,
                           user_service:UserService=Depends(get_user_service),):
    return await user_service.update_post_by_user(post_id,post_update, request)






