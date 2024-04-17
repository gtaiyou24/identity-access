from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateProviderUserCommand:
    email_address: str

    @staticmethod
    def github(user: dict, emails: list[dict]) -> AuthenticateProviderUserCommand:
        email_address = user['email']
        if email_address is None:
            email_address = emails[0]['email']
            for e in emails:
                if e['primary']:
                    email_address = e['email']
        return AuthenticateProviderUserCommand(email_address=email_address)
