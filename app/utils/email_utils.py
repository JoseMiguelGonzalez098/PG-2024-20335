from flask_mail import Message
from flask import url_for

def send_confirmation_email(user_email):
    from app import mail  # Importar aquí para evitar el ciclo
    confirm_url = url_for('mailer_bp.confirm_email', email=user_email, _external=True)
    subject = "Confirma tu cuenta"
    body = f"Por favor, confirma tu cuenta haciendo clic en el siguiente enlace: {confirm_url}"

    msg = Message(subject, recipients=[user_email])
    msg.body = body
    mail.send(msg)
