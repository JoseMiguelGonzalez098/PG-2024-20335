from flask_mail import Message
from flask import url_for
from app import mail

def send_confirmation_email(user_email):
    confirm_url = url_for('mailer_bp.confirm_email', email=user_email, _external=True)  # Genera la URL de confirmación con el correo
    subject = "Confirma tu cuenta"
    body = f"Por favor, confirma tu cuenta haciendo clic en el siguiente enlace: {confirm_url}"

    msg = Message(subject, recipients=[user_email])
    msg.body = body
    mail.send(msg)
