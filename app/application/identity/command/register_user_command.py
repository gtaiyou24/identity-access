from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class RegisterUserCommand:
    email_address: str
    plain_password: str
    first_name: str
    last_name: str
