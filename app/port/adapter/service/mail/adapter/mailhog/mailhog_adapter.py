import smtplib
from email.mime.text import MIMEText

from domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailHogAdapter(MailDeliveryAdapter):
    def send(self, to: EmailAddress, subject: str, message: str) -> None:
        mail = MIMEText(message, 'html')
        mail['Subject'] = subject
        mail['From'] = 'hello@epic-bot.com'
        mail['To'] = to.address

        smtp = smtplib.SMTP(host="mailhog", port=1025)
        smtp.sendmail('hello@epic-bot.com', to.address, mail.as_string())
        smtp.close()
