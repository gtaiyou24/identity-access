from fastapi import Form
from typing_extensions import Annotated


class RegisterUserRequest:
    def __init__(self,
                 email_address: Annotated[str, Form()],
                 password: Annotated[str, Form()],
                 first_name: Annotated[str, Form()],
                 last_name: Annotated[str, Form()]):
        self.email_address = email_address
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
