import email
import smtplib
import imaplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from credentials import login, password


class Gmail:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.smtp = "smtp.gmail.com"
        self.imap = "imap.gmail.com"

    def send_email(self, subject: str, recipients: list, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        ms = smtplib.SMTP('smtp.gmail.com', 587)
        ms.ehlo()
        ms.starttls()
        ms.ehlo()
        ms.login(self.login, self.password)
        ms.sendmail(self.login, msg['To'], msg.as_string())
        ms.quit()

    def recieve_email(self, header: str):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()
        return email_message


if __name__ == '__main__':

    gmail = Gmail(login, password)

    gmail.send_email('test', ['hello@world.com'], 'Hello')
