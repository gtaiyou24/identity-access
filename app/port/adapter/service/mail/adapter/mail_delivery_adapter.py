import abc

from domain.model.user import EmailAddress


class MailDeliveryAdapter(abc.ABC):
    @abc.abstractmethod
    def send(self, to: EmailAddress, subject: str, message: str) -> None:
        pass
