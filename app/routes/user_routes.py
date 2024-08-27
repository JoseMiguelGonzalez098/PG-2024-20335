from flask import Blueprint, jsonify, request
from app.models import Usuario

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/usuario', methods=['GET'])
def get_usuario_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "No email provided"}), 400

    # Buscar el usuario por correo
    usuario = Usuario.query.filter_by(correo=email).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404

    # Preparar la respuesta en formato JSON
    usuario_info = {
        "id": usuario.id,
        "correo": usuario.correo,
        "videos": [
            {
                "id": video.id,
                "traduccion": video.traduccion,
                "favoritos": video.favoritos,
                "video": video.video
            } for video in usuario.videos
        ]
    }

    return jsonify(usuario_info), 200
