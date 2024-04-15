from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta

from domain.model.user import EmailAddress


@dataclass(init=True, frozen=True)
class Token:
    class Name(enum.Enum):
        VERIFICATION = '検証トークン'
        PASSWORD_RESET = 'パスワードリセットトークン'

        def generate(self, email_address: EmailAddress) -> Token:
            return Token(self, email_address, str(uuid.uuid4()), datetime.utcnow() + timedelta(minutes=10))

    name: Name
    email_address: EmailAddress
    value: str
    expires: datetime

    def __hash__(self):
        return hash(self.name)

    def is_(self, name: Name) -> bool:
        return self.name == name

    def has_expired(self) -> bool:
        return self.expires < datetime.utcnow()
