from flask import Blueprint, jsonify, request
from app.models import User, Video, Traduccion
from app import db
from app.utils.email_utils import send_confirmation_email

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/usuario', methods=['GET'])
def get_usuario_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "No email provided"}), 400

    # Buscar el usuario por correo
    usuario = User.query.filter_by(mail=email).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404

    # Preparar la respuesta en formato JSON con los datos del usuario, videos y traducciones
    usuario_info = {
        "id": usuario.id,
        "mail": usuario.mail,
        "streak": usuario.streak,
        "quetzalito": usuario.quetzalito,
        "videos": [
            {
                "id": video.id,
                "traduction_esp": video.traduction_esp,
                "sentence_lensegua": video.sentence_lensegua,
                "video": video.video
            } for video in usuario.videos
        ],
        "traducciones": [
            {
                "id": traduccion.id,
                "sentence_lensegua": traduccion.sentence_lensegua,
                "traduction_esp": traduccion.traduction_esp
            } for traduccion in usuario.traducciones
        ]
    }

    return jsonify(usuario_info), 200

@user_bp.route('/login', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    if not email:
        return jsonify({"error": "No email provided"}), 400

    # Buscar el usuario por correo
    usuario = User.query.filter_by(mail=email).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404
    if usuario.password != password:
        return jsonify({"error": "Password incorrect"}), 404

    # Preparar la respuesta en formato JSON con los datos del usuario, videos y traducciones
    responce = {
        "id": usuario.id
    }

    return jsonify(responce), 200

@user_bp.route('/signup', methods=['POST'])
def singup():
    email = request.args.get('email')
    password = request.args.get('password')
    quezalito = request.args.get('quezalito')
    if not email:
        return jsonify({"error": "No email provided"}), 400
    
    # Buscar el usuario por correo
    usuario = User.query.filter_by(mail=email).first()
    if usuario:
        return jsonify({"error": "User already exist"}), 404
    
    # Crear el usuario
    nuevo_usuario = User(
        mail=email,
        password=password,
        streak=0,  # Ejemplo: podrías ajustar el valor de streak
        quetzalito=quezalito
    )

    # Enviar correo de confirmación
    send_confirmation_email(email)

    # Agregar el usuario a la sesión
    db.session.add(nuevo_usuario)

    # Preparar la respuesta en formato JSON con los datos del usuario, videos y traducciones
    responce = {
        "id": usuario.id
    }

    return jsonify(responce), 200

@user_bp.route('/change_password', methods=['POST'])
def change_password():
    id_user = request.args.get('id_user')
    new_password = request.args.get('new_password')
   
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404
    
    if not new_password:
        return jsonify({"error": "No new password provided"}), 400

    # Cambiar la contraseña
    usuario.password = new_password

    # Preparar la respuesta en formato JSON con los datos del usuario, videos y traducciones
    responce = {
        "id": usuario.id
    }

    return jsonify(responce), 200

@user_bp.route('/forgot_password', methods=['GET'])
def forgot_password():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "No email provided"}), 400

    # Buscar el usuario por correo
    usuario = User.query.filter_by(mail=email).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404

    # Enviar correo de confirmación
    send_confirmation_email(email)

    # Preparar la respuesta en formato JSON con los datos del usuario, videos y traducciones
    responce = {
        "id": usuario.id
    }

    return jsonify(responce), 200