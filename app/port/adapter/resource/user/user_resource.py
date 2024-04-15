from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer

from domain.model.user import User
from port.adapter.resource.auth.auth_resource import get_current_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/users',
    tags=['User']
)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
