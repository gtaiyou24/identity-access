from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ResetPasswordCommand:
    token: str
    password: str
