from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class AuthenticateUserCommand:
    email_address: str
    password: str
