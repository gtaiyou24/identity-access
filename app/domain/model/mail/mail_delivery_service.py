import abc

from domain.model.user import EmailAddress


class MailDeliveryService(abc.ABC):
    @abc.abstractmethod
    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        pass
