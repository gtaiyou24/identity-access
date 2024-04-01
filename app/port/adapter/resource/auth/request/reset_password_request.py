from pydantic import BaseModel, Field


class ResetPasswordRequest(BaseModel):
    email_address: str = Field(title="メールアドレス")
    password: str = Field(title="パスワード")
