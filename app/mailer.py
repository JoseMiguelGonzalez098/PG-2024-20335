from flask_mail import Mail, Message
from app import create_app

# Inicializar Flask-Mail
mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_email(subject, recipients, body, html=None):
    msg = Message(subject, recipients=recipients, body=body, html=html)
    mail.send(msg)
