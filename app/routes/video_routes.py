from flask import Blueprint, jsonify, request
from app.models import User, Video
from werkzeug.utils import secure_filename
from app import db  # Importar db para interactuar con la base de datos
from flask import send_from_directory

video_bp = Blueprint('video_bp', __name__)

# Ruta para almacenar los videos
VIDEO_STORAGE_PATH = '/srv/web-apps/api-central/videos/'

@video_bp.route('/send_video', methods=['POST'])
def send_video():
    # Obtener id de usuario y archivo de video
    id_user = request.form.get('id_user')
    video_file = request.files.get('video')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404

    # Verificar que se ha proporcionado un archivo de video
    if not video_file:
        return jsonify({"error": "No video provided"}), 400

    # Asegurarse de que el nombre del archivo es seguro para usarlo en el sistema de archivos
    filename = secure_filename(video_file.filename)
    
    # Crear la ruta completa para guardar el archivo
    save_path = os.path.join(VIDEO_STORAGE_PATH, filename)

    # Guardar el archivo en la ruta especificada
    try:
        video_file.save(save_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save video: {str(e)}"}), 500

    # Crear un nuevo objeto Video y guardar la ruta en la base de datos
    new_video = Video(
        usuario_id=id_user,
        video=save_path,
        traduccion=None,  # Puedes ajustar esto según tus necesidades
        favoritos=False
    )

    db.session.add(new_video)
    db.session.commit()

    return jsonify({"message": "Video uploaded successfully", "video_id": new_video.id}), 200
# Ruta: /report_video (GET)
@video_bp.route('/report_video', methods=['GET'])
def report_video():
    id_user = request.args.get('id_user')
    id_video = request.args.get('id_video')
    report_message = request.args.get('report_message')
    report_img = request.args.get('report_img')  # Se asume que es una URL o path al archivo de imagen

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404
    
    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"error": "Video not found"}), 404

    # Aquí podrías implementar lógica para almacenar o manejar el reporte.
    # Por simplicidad, solo devolvemos un mensaje de éxito.
    
    return jsonify({"message": "Report submitted successfully"}), 200

# Ruta: /fav_video (POST)
@video_bp.route('/fav_video', methods=['POST'])
def fav_video():
    id_user = request.form.get('id_user')
    id_video = request.form.get('id_video')

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"error": "User not found"}), 404
    
    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"error": "Video not found"}), 404
    
    video.favoritos = True
    db.session.commit()

    return jsonify({"message": "Video marked as favorite"}), 200

# Ruta: /remove_video (DELETE)
@video_bp.route('/remove_video', methods=['DELETE'])
def remove_video():
    id_video = request.args.get('id_video')

    video = Video.query.filter_by(id=id_video).first()
    if not video:
        return jsonify({"error": "Video not found"}), 404

    db.session.delete(video)
    db.session.commit()

    return jsonify({"message": "Video deleted successfully"}), 200

@video_bp.route('/download_video/<path:filename>', methods=['GET'])
def download_video(filename):
    video_directory = "/srv/web-apps/api-central/videos/"
    return send_from_directory(directory=video_directory, path=filename, as_attachment=True)
