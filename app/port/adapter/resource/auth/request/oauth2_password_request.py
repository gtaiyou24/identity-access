from fastapi import Form
from typing_extensions import Annotated


class OAuth2PasswordRequest:
    def __init__(self,
                 email_address: Annotated[str, Form()],
                 password: Annotated[str, Form()]):
        self.email_address = email_address
        self.password = password
