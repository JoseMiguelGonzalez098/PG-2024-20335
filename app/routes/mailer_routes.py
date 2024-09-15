from flask import Blueprint, jsonify, request, url_for
from app.models import User, db
from flask_mail import Message

mailer_bp = Blueprint('mailer_bp', __name__)

@mailer_bp.route('/confirm', methods=['POST'])
def confirm_email():
    email = request.args.get('email')  # Obtenemos el correo desde la URL
    if not email:
        return jsonify({"message": "Correo no proporcionado"}), 400

    # Verificar si el usuario existe
    user = User.query.filter_by(mail=email).first()
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    # Confirmar el usuario si no está confirmado
    if user.confirmed:
        return jsonify({"message": "La cuenta ya está confirmada."}), 200

    user.confirmed = True
    db.session.commit()

    # Mueve la importación de mail aquí
    from app import mail  # Importamos mail localmente
    msg = Message("Tu cuenta ha sido confirmada", recipients=[email])
    mail.send(msg)

    return jsonify({"message": "Tu cuenta ha sido confirmada exitosamente."}), 200
