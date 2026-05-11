from auth.utils import encode_jwt
from users.schemas import UserRead
from auth.utils import encode_jwt
from src.config import settings
from datetime import datetime, timedelta
from fastapi import Response

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

async def create_jwt(token_type:str,token_data:dict,
                     expire_minutes: int = settings.jwt_settings.access_token_expire_minutes,
                     expire_timedelta: timedelta | None = None ) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(**token_data)
    return await encode_jwt(payload=jwt_payload,
                            expire_minutes=expire_minutes,
                            expire_delta=expire_timedelta)


async def create_access_token(auth_user: UserRead|None = None, user_id = None) -> str:
    jwt_payload = {"sub": str(auth_user.id if auth_user else user_id),}
    token = await create_jwt(token_type=ACCESS_TOKEN_TYPE,token_data=jwt_payload,
                       expire_minutes=settings.jwt_settings.access_token_expire_minutes,)

    return token

async def create_refresh_token(auth_user: UserRead,):
    jwt_payload = {"sub": str(auth_user.id),}
    return await create_jwt(token_type=REFRESH_TOKEN_TYPE, token_data=jwt_payload,
                      expire_timedelta=timedelta(days=settings.jwt_settings.refresh_token_expire_days))

