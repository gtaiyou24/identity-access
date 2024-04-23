from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from application.identity.dpo import UserDpo
from port.adapter.resource.auth.auth_resource import get_current_active_user
from port.adapter.resource.user.response import UserJson

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get("/me", response_model=UserJson)
async def read_users_me(current_user: UserDpo = Depends(get_current_active_user)) -> UserJson:
    return UserJson.from_(current_user)
