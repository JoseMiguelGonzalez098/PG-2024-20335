from app import app, db
from models import Usuario, Video

with app.app_context():
    # Crear el usuario
    nuevo_usuario = Usuario(
        correo='user-dummy@se-chapinas.com',
        contrasena='123'
    )

    # Ubicación de los videos
    video_paths = [
        '/srv/web-apps/api-central/videos/prueba1-2024.mp4',
        '/srv/web-apps/api-central/videos/prueba2-2024.mp4',
        '/srv/web-apps/api-central/videos/prueba3-2024.mp4'
    ]

    # Crear los videos asociados al usuario
    videos = [
        Video(traduccion='video1', favoritos=True, video=video_paths[0]),
        Video(traduccion='video2', favoritos=True, video=video_paths[1]),
        Video(traduccion='video3', favoritos=False, video=video_paths[2])
    ]

    # Asociar los videos al usuario
    nuevo_usuario.videos = videos

    # Agregar a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    print("Usuario y videos creados exitosamente.")
