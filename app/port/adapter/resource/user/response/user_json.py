from __future__ import annotations

from pydantic import BaseModel, Field

from application.identity.dpo import UserDpo


class UserJson(BaseModel):
    class FullName(BaseModel):
        first_name: str = Field(title='氏名')
        last_name: str = Field(title='姓名')

    email_address: str = Field(title='メールアドレス')
    full_name: FullName = Field(title='名前', description='フルネームの名前')

    @staticmethod
    def from_(dpo: UserDpo) -> UserJson:
        return UserJson(
            email_address=dpo.user.email_address.address,
            full_name=UserJson.FullName(
                first_name=dpo.user.full_name.first_name,
                last_name=dpo.user.full_name.last_name,
            )
        )