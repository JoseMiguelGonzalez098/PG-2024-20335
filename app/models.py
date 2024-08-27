from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    traduccion = db.Column(db.Text, nullable=True)
    favoritos = db.Column(db.Boolean, default=False)
    video = db.Column(db.String(255), nullable=False)  # Aquí almacenarás la ruta del video

    usuario = relationship("Usuario", backref="videos")

    def __repr__(self):
        return f'<Video {self.id} de usuario {self.usuario_id}>'