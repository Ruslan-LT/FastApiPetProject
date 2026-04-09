from users.schemas import UserRead

async def convert_user_model(user):
    return UserRead.model_validate(user)