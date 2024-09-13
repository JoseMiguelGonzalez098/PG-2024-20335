from flask import Blueprint, jsonify, request, url_for
from app.models import Usuario, db
from flask_mail import Message
from app import mail

mailer_bp = Blueprint('mailer_bp', __name__)  # Cambia user_bp a mailer_bp

def send_confirmation_email(user_email):
    confirm_url = url_for('mailer_bp.confirm_email', email=user_email, _external=True)  # Genera la URL de confirmación con el correo
    subject = "Confirma tu cuenta"
    body = f"Por favor, confirma tu cuenta haciendo clic en el siguiente enlace: {confirm_url}"

    msg = Message(subject, recipients=[user_email])
    msg.body = body
    mail.send(msg)

@mailer_bp.route('/confirm', methods=['GET'])
def confirm_email():
    email = request.args.get('email')  # Obtenemos el correo desde la URL
    if not email:
        return jsonify({"error": "Correo no proporcionado"}), 400

    # Verificar si el usuario existe
    user = Usuario.query.filter_by(correo=email).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Verificar si el usuario ya está confirmado
    if user.confirmed:
        return jsonify({"message": "La cuenta ya está confirmada."}), 200
    
    # Confirmar el usuario si no está confirmado
    user.confirmed = True
    db.session.commit()
    return jsonify({"message": "Tu cuenta ha sido confirmada exitosamente."}), 200
