import re
from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, eq=True, frozen=True)
class EmailAddress:
    address: str

    def __init__(self, address: str):
        assert address, 'メールアドレスは必須です。'
        assert 0 < len(address) <= 100, 'メールアドレスは100文字以下である必要があります。'
        assert re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", address), 'メールアドレスが不正です。'

        super().__setattr__("address", address)
