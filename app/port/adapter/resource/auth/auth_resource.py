from di import DIContainer
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from application.identity import IdentityApplicationService
from application.identity.command import AuthenticateUserCommand, RegisterUserCommand, ForgotPasswordCommand, \
    ResetPasswordCommand
from domain.model.user import User
from port.adapter.resource.auth import JWTEncoder
from port.adapter.resource.auth.request import OAuth2PasswordRequest, ResetPasswordRequest, VerifyRequest, \
    RegisterUserRequest, ForgotPasswordRequest
from port.adapter.resource.auth.response import Token, UserDescriptorJson

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
        payload = JWTEncoder.decode(token)
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


@router.post("/user/register", response_model=UserDescriptorJson)
def register_user(request: RegisterUserRequest):
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    dpo = application_service.register_user(RegisterUserCommand(
        request.email_address,
        request.password
    ))
    return UserDescriptorJson.from_(dpo)


@router.post("/verify-email/{token}")
def verify_email(token: str):
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    application_service.verify_email(token)


@router.post("/token", response_model=Token)
def token(request: OAuth2PasswordRequest) -> Token:
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
def forgot_password(request: ForgotPasswordRequest):
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    application_service.forgot_password(ForgotPasswordCommand(request.email_address))


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    application_service.reset_password(ResetPasswordCommand(request.token, request.password))
