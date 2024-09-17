from flask import Blueprint, jsonify, request
from app.models import User, Video
from werkzeug.utils import secure_filename
from app import db  # Importar db para interactuar con la base de datos
from flask import send_from_directory
from flask_uploads import UploadSet

video_bp = Blueprint('video_bp', __name__)

# Ruta para almacenar los videos
VIDEO_STORAGE_PATH = '/srv/web-apps/api-central/videos/'
IMAGES_STORAGE_PATH = '/srv/web-apps/api-central/images/'

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@video_bp.route('/send_video', methods=['POST'])
def send_video():
    # Obtener id de usuario y archivo de video
    id_user = request.form.get('id_user')
    video_file = request.files.get('video')

    # Verificar que el usuario exista
    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "User not found"}), 404

    # Verificar que se ha proporcionado un archivo de video
    if not video_file or not allowed_file(video_file.filename):
        return jsonify({"message": "No video provided or invalid file type"}), 400

    # Asegurarse de que el nombre del archivo es seguro para usarlo en el sistema de archivos
    filename = secure_filename(video_file.filename)
    
    # Evitar sobrescribir archivos con el mismo nombre añadiendo una marca de tiempo
    unique_filename = f"{id_user}_{int(time.time())}_{filename}"
    save_path = os.path.join(VIDEO_STORAGE_PATH, unique_filename)

    # Guardar el archivo en la ruta especificada
    try:
        video_file.save(save_path)
    except Exception as e:
        return jsonify({"message": f"Failed to save video: {str(e)}"}), 500

    sentence_lensegua = "Texto en lensegua"

    # Procesamiento de la oracion para obtener la traducción
    traduction_esp = "Traducción del video en español"

    # Crear un nuevo objeto Video y guardar la ruta en la base de datos
    new_video = Video(
        id_user=id_user,
        traduction_esp=traduction_esp,
        sentence_lensegua=sentence_lensegua,
        video=save_path
    )

    db.session.add(new_video)
    db.session.commit()

    return jsonify(
        {
            "id_video": new_video.id, 
            "traduction_esp": new_video.traduction_esp, 
            "sentence_lensegua": new_video.sentence_lensegua
        }
    ), 200

# Ruta: /report_video (POST)
@video_bp.route('/report_video', methods=['POST'])
def report_video():
    data = request.get_json()
    id_user = data.get('id_user')
    id_video = data.get('id_video')
    report_message = data.get('report_message')
    report_img = data.get('report_img')  # Se asume que es una URL o path al archivo de imagen

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"message": "Video no encontardo"}), 404

    # Aquí podrías implementar lógica para almacenar o manejar el reporte.
    # Por simplicidad, solo devolvemos un mensaje de éxito.
    
    return jsonify({"message": "Se ha reportado el video exitosamente"}), 200

# Ruta: /fav_video (POST)
@video_bp.route('/fav_video', methods=['POST'])
def fav_video():
    data = request.get_json()
    id_user = data.get('id_user')
    id_video = data.get('id_video')
    prev_video = request.files.get('prev_video')  # Cambiar a request.files.get()

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"message": "No se ha dado video"}), 404
    
    if not prev_video:  # Verificar que se ha proporcionado una imagen
        return jsonify({"message": "No se ha proporcionado imagen de preview"}), 400
    
    # Asegurarse de que el nombre del archivo es seguro para usarlo en el sistema de archivos
    filename = secure_filename(prev_video.filename)

    # Definir la ruta para guardar la imagen
    save_path = os.path.join(IMAGES_STORAGE_PATH, filename)

    # Guardar la imagen en la ruta especificada
    try:
        prev_video.save(save_path)
    except Exception as e:
        return jsonify({"message": f"Failed to save image: {str(e)}"}), 500

    # Marcar el video como favorito
    video.is_favorite = True
    db.session.commit()

    return jsonify({"message": "Video marked as favorite"}), 200

@video_bp.route('/remove_fav_video', methods=['POST'])
def remove_fav_video():
    data = request.get_json()
    id_user = data.get('id_user')
    id_video = data.get('id_video')

    usuario = User.query.filter_by(id=id_user).first()
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    video = Video.query.filter_by(id=id_video, id_user=id_user).first()
    if not video:
        return jsonify({"message": "No se ha dado video"}), 404

    # Eliminar la imagen previa existente si hay una
    if video.prev_image:
        try:
            os.remove(video.prev_image)
        except Exception as e:
            return jsonify({"message": f"Failed to delete existing image: {str(e)}"}), 500

    # Marcar el video como no favorito
    video.is_favorite = False
    db.session.commit()

    return jsonify({"message": "Video removido de favoritos e imagen eliminada"}), 200

# Ruta: /remove_video (DELETE)
@video_bp.route('/remove_video', methods=['DELETE'])
def remove_video():
    id_video = request.args.get('id_video')

    video = Video.query.filter_by(id=id_video).first()
    if not video:
        return jsonify({"message": "Video not found"}), 404

    db.session.delete(video)
    db.session.commit()

    return jsonify({"message": "Video deleted successfully"}), 200

@video_bp.route('/download_video/<path:filename>', methods=['POST'])
def download_video(filename):
    data = request.get_json()
    video_directory = "/srv/web-apps/api-central/videos/"
    return send_from_directory(directory=video_directory, path=filename, as_attachment=True)

@video_bp.route('/download_image/<path:filename>', methods=['POST'])
def download_image(filename):
    data = request.get_json()
    image_directory = "/srv/web-apps/api-central/images/"
    return send_from_directory(directory=image_directory, path=filename, as_attachment=True)