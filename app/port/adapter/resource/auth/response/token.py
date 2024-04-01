from __future__ import annotations

from datetime import timedelta, datetime, timezone

from jose import jwt
from pydantic import BaseModel

from application.identity.dpo import UserDpo
from port.adapter.resource.auth import JWT

# to get a string like this run:
# openssl rand -hex 32
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str

    @staticmethod
    def generate(dpo: UserDpo) -> Token:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = JWT.encode({
            "sub": dpo.user.email_address.address,
            'exp': expire
        })
        return Token(access_token=access_token, token_type="bearer")
