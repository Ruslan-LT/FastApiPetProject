from datetime import timedelta, datetime, timezone
import jwt
from src.config import settings

async def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt_settings.private_key_path.read_text(),
    algorithm: str = settings.jwt_settings.algorithm,
    expire_delta: timedelta | None = None,
    expire_minutes: int = settings.jwt_settings.access_token_expire_minutes,
):
    to_encode = payload.copy()

    time_now = datetime.now(timezone.utc)

    if expire_delta:
        expire = time_now + expire_delta
    else:
        expire = time_now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=int(expire.timestamp()),
        iat=int(time_now.timestamp()),
    )

    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded_jwt

async def decode_jwt(encoded_jwt: str | bytes, public_key:str=settings.jwt_settings.public_key_path.read_text(),
                     algorithm=settings.jwt_settings.algorithm):
    decoded = jwt.decode(encoded_jwt, public_key, algorithms=[algorithm])
    return decoded

