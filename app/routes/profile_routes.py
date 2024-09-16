from flask import Blueprint, jsonify, request, url_for
from app import db
from app.models import User, Video, Traduccion

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/get_user_info', methods=['POST'])
def get_user_info():
    data = request.get_json()
    id_user = data.get('id_user')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    # Obtener videos y traducciones favoritas del usuario
    videos_fav = Video.query.filter_by(id_user=id_user).all()
    traducciones_fav = Traduccion.query.filter_by(id_user=id_user).all()

    # Preparar la respuesta con la información del usuario
    user_info = {
        "mail": usuario.mail,
        "streak": usuario.streak,
        "quetzalito": usuario.quetzalito,
        "videos_fav": [{"sentence_lensegua":video.sentence_lensegua,"traduction_esp": video.traduction_esp, "id_video": video.id, "prev_image": video.prev_image} for video in videos_fav],
        "traductions_fav": [{"traduction": trad.traduction_esp, "sentence_lensegua": trad.sentence_lensegua, "id_traduction": trad.id} for trad in traducciones_fav]
    }

    return jsonify(user_info), 200

@profile_bp.route('/get_video', methods=['POST'])
def get_video():
    data = request.get_json()
    id_user = data.get('id_user')
    id_video = data.get('id_video')

    # Verificar que el usuario y el video existan
    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"message": "Video not found or does not belong to the user"}), 404

    # Crear la URL que apunta a la ruta para descargar el video
    download_url = url_for('video_bp.download_video', filename=video.video.split('/')[-1], _external=True)

    return jsonify({"video": download_url}), 200

@profile_bp.route('/get_image', methods=['POST'])
def get_image():
    data = request.get_json()
    id_user = data.get('id_user')
    id_video = data.get('id_video')

    # Verificar que el usuario y el video existan
    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"message": "Video not found or does not belong to the user"}), 404

    # Crear la URL que apunta a la ruta para descargar la imagen
    download_url = url_for('video_bp.download_image', filename=video.prev_image.split('/')[-1], _external=True)

    return jsonify({"image": download_url}), 200

@profile_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    id_user = request.form.get('id_user')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    # Eliminar el usuario y todas las entidades relacionadas
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

@profile_bp.route('/add_streak', methods=['POST'])
def add_streak():
    data = request.get_json()
    id_user = data.get('id_user')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    # Incrementar el streak del usuario
    usuario.streak += 1
    db.session.commit()

    return jsonify({"message": "Streak incremented", "streak": usuario.streak}), 200
