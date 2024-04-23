from __future__ import annotations

from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateProviderUserCommand:
    email_address: str

    @staticmethod
    def github(user: dict, emails: list[dict]) -> AuthenticateProviderUserCommand:
        default_email = user['email'] or emails[0]['email']
        primary_email = None
        for e in emails:
            if e['primary']:
                primary_email = e['email']
        return AuthenticateProviderUserCommand(email_address=primary_email or default_email)
