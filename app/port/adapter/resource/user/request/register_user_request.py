from pydantic import BaseModel, Field


class RegisterUserRequest(BaseModel):
    email_address: str = Field(title='メールアドレス')
    password: str = Field(title='パスワード')
    first_name: str = Field(title='氏名')
    last_name: str = Field(title='姓名')
