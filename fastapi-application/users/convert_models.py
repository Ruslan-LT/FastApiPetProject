from users.schemas import UserRead

async def convert_user_model(user, Model):
    return Model.model_validate(user)