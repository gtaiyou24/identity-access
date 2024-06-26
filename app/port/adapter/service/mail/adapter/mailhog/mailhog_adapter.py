import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html2text import html2text

from domain.model.user import EmailAddress
from port.adapter.service.mail.adapter import MailDeliveryAdapter


class MailHogAdapter(MailDeliveryAdapter):
    _FROM = 'hello@epic-bot.com'

    def __init__(self):
        self.__smtp = smtplib.SMTP(host="mailhog", port=1025)

    def send(self, to: EmailAddress, subject: str, html: str) -> None:
        mail = MIMEMultipart('alternative')
        mail['Subject'] = subject
        mail['From'] = self._FROM
        mail['To'] = to.address

        mail.attach(MIMEText(html2text(html), 'plain'))
        mail.attach(MIMEText(html, 'html'))

        self.__smtp.sendmail(self._FROM, to.address, mail.as_string())
