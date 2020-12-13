from flask_mail import Mail, Message
from flask import url_for
from src.app.config import MAIL_USERNAME


class MailSender:

    def __init__(self, app):
        self._mail = Mail(app)

    def __call__(self, email, token):
        # get he url to include in the message
        link = url_for('confirm_email', token=token, _external=True)
        # write the message
        msg = self._write_msg(email, link)
        # send the email
        return self._mail.send(msg)
        
    @staticmethod
    def _write_msg(email, link):
        msg = Message('Confirm email', sender=MAIL_USERNAME, recipients=[email])
        msg.body = f'Your link is: {link}'
        return msg
