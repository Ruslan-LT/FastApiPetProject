from typing import Annotated
from fastapi import (Depends, APIRouter, Response, Request,  status, Path)
from users.schemas import  UserCreate, UserRead, UserUpdate, Token
from users.security import get_auth_username, COOKIE_REFRESH_TOKEN_KEY, COOKIE_ACCESS_TOKEN_KEY
from users.service import UserService
from users.dependencies import get_user_service, check_user_have_access_token
from news.schemas import PostRead, PostUpdate
from auth.tokens_check_dependencies import jwt_refresh_token_check_dependency, jwt_access_token_check_dependency
from auth.utils import decode_jwt
from auth.helpers import create_access_token
user_router = APIRouter(tags=["users"],
                        prefix="/users",)

@user_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED,)
async def create_user(user: UserCreate, response: Response, request: Request, user_service:UserService=Depends(get_user_service)):
    return await user_service.create_user_account(user,response,request)

@user_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def user_logout(response: Response,
                      request: Request,
                      user_service:UserService=Depends(get_user_service)):
    return await user_service.logout_user_account(response, request)

@user_router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK,
                 dependencies=[Depends(check_user_have_access_token), Depends(jwt_refresh_token_check_dependency),
                               Depends(jwt_access_token_check_dependency)])
async def get_current_user(response: Response,
                      request: Request,
                      user_service:UserService=Depends(get_user_service)):
    return await user_service.read_auth_user_account(request)

@user_router.put("/me", response_model=UserRead, status_code=status.HTTP_200_OK,
                 dependencies=[Depends(check_user_have_access_token), Depends(jwt_refresh_token_check_dependency),
                               Depends(jwt_access_token_check_dependency)])
async def update_user_account_data(user_update:UserUpdate,
                                   request: Request,
                                   user_service:UserService=Depends(get_user_service)):

    return await user_service.update_user_account(user_update, request)

@user_router.delete("/my_post",status_code=status.HTTP_204_NO_CONTENT,
                    dependencies=[Depends(check_user_have_access_token), Depends(jwt_refresh_token_check_dependency),
                                  Depends(jwt_access_token_check_dependency)])
async def delete_post_by_user(post_id: int,
                              request: Request,
                              user_service:UserService=Depends(get_user_service)):

     await user_service.delete_post_by_user(request,post_id)

@user_router.put("/my_post/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK,
                 dependencies=[Depends(check_user_have_access_token), Depends(jwt_refresh_token_check_dependency),
                               Depends(jwt_access_token_check_dependency)])
async def update_user_post(post_id:Annotated[int,Path()],
                           request:Request,
                           post_update: PostUpdate,
                           user_service:UserService=Depends(get_user_service),):
    return await user_service.update_post_by_user(post_id,post_update, request)

@user_router.post("/login", response_model=Token)
async def login_jwt(request: Request, response: Response,auth_user:Annotated[UserRead, Depends(get_auth_username)],
                     user_service:UserService=Depends(get_user_service)):
    return await user_service.login_user_account_jwt(auth_user, response, request)

@user_router.post("/refresh", status_code=status.HTTP_200_OK,)
async def refresh_jwt(request: Request, response: Response,
                      user_service: UserService = Depends(get_user_service)
                      ):
    return await user_service.refresh_jwt_access(request, response)







