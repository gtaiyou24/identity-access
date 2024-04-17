from __future__ import annotations

from datetime import timedelta, datetime, timezone

from pydantic import BaseModel

from application.identity.dpo import UserDpo
from port.adapter.resource.auth import JWTEncoder


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    @staticmethod
    def generate(dpo: UserDpo) -> Token:
        now = datetime.now(timezone.utc)
        access_token = JWTEncoder.encode({
            "sub": dpo.user.email_address.address,
            'exp': now + timedelta(minutes=30)
        })
        refresh_token = JWTEncoder.encode({
            "sub": dpo.user.email_address.address,
            'exp': now + timedelta(minutes=60)
        })
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
