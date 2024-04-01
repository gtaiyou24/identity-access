from __future__ import annotations

import uuid
from dataclasses import dataclass

from domain.model.tenant import TenantId, RegistrationInvitation


@dataclass(init=True, unsafe_hash=False, eq=False)
class Tenant:
    """テナント"""
    id: TenantId
    name: str
    description: str
    registration_invitations: set[RegistrationInvitation]
    _active: bool

    @staticmethod
    def provisioned(id: TenantId, name: str, description: str) -> Tenant:
        """テナントを新規作成する"""
        return Tenant(id, name, description, set(), True)

    @property
    def is_active(self) -> bool:
        return self._active

    def active(self) -> None:
        if not self._active:
            self._active = True

    def is_registration_available_through(self, invitation_id: str):
        """該当招待状で登録可能かどうか判定する"""
        assert self.is_active, "テナントがアクティブではありません。"

        invitation = self.invitation_of(invitation_id)
        return False if invitation is None else invitation.is_available()

    def offer_registration_invitation(self, description: str) -> RegistrationInvitation:
        """登録用招待状を発行する"""
        assert self.is_active, "テナントがアクティブではありません。"
        assert not self.is_registration_available_through(description), "招待状はすでに存在します。"

        invitation = RegistrationInvitation(self.id, str(uuid.uuid4()), description)
        self.registration_invitations.add(invitation)

        return invitation

    def invitation_of(self, invitation_id) -> RegistrationInvitation | None:
        for invitation in self.registration_invitations:
            if invitation.is_identified_by(invitation_id):
                return invitation
        return None
