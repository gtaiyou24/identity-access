from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class FullName:
    first_name: str
    last_name: str
