import abc


class EncryptionService(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, plain_value: str) -> str:
        pass

    @abc.abstractmethod
    def verify(self, plain_value, hashed_value) -> bool:
        pass
