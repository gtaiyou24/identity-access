from __future__ import annotations

from dataclasses import dataclass

from domain.model import DomainRegistry
from domain.model.user import EmailAddress, FullName, EncryptionService


@dataclass(init=False, eq=False)
class User:
    _email_address: EmailAddress
    _encrypted_password: str
    _full_name: FullName
    _enable: bool

    def __init__(self, email_address: EmailAddress, encrypted_password, full_name: FullName, enable: bool):
        super().__setattr__("_email_address", email_address)
        super().__setattr__("_encrypted_password", encrypted_password)
        super().__setattr__("_full_name", full_name)
        super().__setattr__("_enable", enable)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.email_address == other.email_address

    def __hash__(self):
        return hash(self.email_address)

    @staticmethod
    def new(email_address: EmailAddress, plain_password: str, full_name: FullName) -> User:
        return User(
            email_address,
            DomainRegistry.resolve(EncryptionService).encrypt(plain_password),
            full_name,
            True
        )

    @property
    def email_address(self) -> EmailAddress:
        return self._email_address

    @property
    def encrypted_password(self) -> str:
        return self._encrypted_password

    @property
    def full_name(self) -> FullName:
        return self._full_name

    @property
    def disabled(self) -> bool:
        return self._enable is False

    @email_address.setter
    def email_address(self, value: EmailAddress) -> None:
        self._email_address = value

    def verify_password(self, plain_password: str) -> bool:
        return DomainRegistry.resolve(EncryptionService).verify(plain_password, self.encrypted_password)

