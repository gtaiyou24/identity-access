from __future__ import annotations

import datetime
from dataclasses import dataclass

from domain.model.tenant import TenantId


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RegistrationInvitation:
    """登録用招待状"""
    tenant_id: TenantId
    invitation_id: str
    description: str | None = None
    starting_on: datetime.datetime | None = None
    until: datetime.datetime | None = None

    def is_identified_by(self, id: str) -> bool:
        if self.invitation_id == id:
            return True
        if self.description is not None:
            return self.description == id
        return False

    def open_end(self) -> RegistrationInvitation:
        return RegistrationInvitation(self.tenant_id, self.invitation_id, self.description, None, None)

    def is_available(self) -> bool:
        """招待状が有効かどうか判定する"""
        if self.starting_on is None and self.until is None:
            return True
        return self.starting_on <= datetime.datetime.now() <= self.until
