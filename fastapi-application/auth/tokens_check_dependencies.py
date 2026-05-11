from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
from users.security import COOKIE_ACCESS_TOKEN_KEY, COOKIE_REFRESH_TOKEN_KEY, COOKIE_LIST
from jwt.exceptions import ExpiredSignatureError
from src.database import session_dependency
from users.security import get_current_token_payload
from users.repository import UserRepository

async def jwt_access_token_check_dependency(request: Request):
    auth_token = request.cookies.get(COOKIE_ACCESS_TOKEN_KEY)
    if auth_token:
        try:
            payload = await get_current_token_payload(str(auth_token))
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

async def jwt_refresh_token_check_dependency(request: Request):
    refresh_token = request.cookies.get(COOKIE_REFRESH_TOKEN_KEY)
    if refresh_token:
        try:
            payload = await get_current_token_payload(refresh_token)
        except ExpiredSignatureError:
            session = session_dependency()
            await UserRepository(session).delete_jwt_refresh_token_by_token_body(refresh_token)
            resp =  Response(status_code=401, content={"detail": "Expired token"})
            for cookie in COOKIE_LIST:
                resp.delete_cookie(cookie)
            return resp
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
