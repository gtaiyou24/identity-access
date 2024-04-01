from passlib.context import CryptContext

from domain.model.user import EncryptionService


class EncryptionServiceImpl(EncryptionService):
    def __init__(self):
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, plain_value: str) -> str:
        return self.__pwd_context.hash(plain_value)

    def verify(self, plain_value, hashed_value) -> bool:
        return self.__pwd_context.verify(plain_value, hashed_value)
