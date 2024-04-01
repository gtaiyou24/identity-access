from di import DIContainer
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from application.identity import IdentityApplicationService
from application.identity.command import AuthenticateUserCommand
from domain.model.user import User
from port.adapter.resource.auth import JWT
from port.adapter.resource.auth.request import OAuth2PasswordRequest, ResetPasswordRequest, VerifyRequest
from port.adapter.resource.auth.response import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = JWT.decode(token)
        email_address: str = payload.get("sub")
        if email_address is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    dpo = application_service.user(email_address)
    if dpo is None:
        raise credentials_exception
    return dpo.user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
def token(request: OAuth2PasswordRequest = Depends()) -> Token:
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    dpo = application_service.authenticate_user(AuthenticateUserCommand(request.email_address, request.password))
    return Token.generate(dpo)


@router.put("/token")
def refresh(current_user: User = Depends(get_current_active_user)) -> None:
    pass


@router.delete("/token")
def revoke(current_user: User = Depends(get_current_active_user)) -> None:
    """ログアウト処理
    ・JWTを Redis から削除する
    """
    pass


@router.post("/verify")
def verify(request: VerifyRequest):
    """指定したトークンが有効か判定する"""
    pass


@router.post("/forgot-password")
def forgot_password() -> None:
    return None


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest) -> None:
    return None
