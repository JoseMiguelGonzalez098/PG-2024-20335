from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Tabla: user
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    streak = db.Column(db.Integer, default=0)  # Se asume que el streak inicia en 0
    quetzalito = db.Column(db.String(120), nullable=True)  # Se asume que puede ser nulo

    # Relación con las otras tablas
    videos = relationship("Video", backref="user", lazy=True)
    traducciones = relationship("Traduccion", backref="user", lazy=True)

    def __repr__(self):
        return f'<User {self.mail}>'

# Tabla: video
class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    traduction_esp = db.Column(db.String(255), nullable=True)
    sentence_lensegua = db.Column(db.String(255), nullable=False)
    video = db.Column(db.String(255), nullable=False)  # Ruta del video

    def __repr__(self):
        return f'<Video {self.id} para usuario {self.id_user}>'

# Tabla: traduccion
class Traduccion(db.Model):
    __tablename__ = 'traduccion'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sentence_lensegua = db.Column(db.String(255), nullable=False)
    traduction_esp = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Traduccion {self.id} para usuario {self.id_user}>'

class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    id = db.Column(db.Integer, primary_key=True)
    id_word = db.Column(db.Integer, nullable=False)  # Este ID no es único
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    def __repr__(self):
        return f'<Dictionary {self.id_word} para usuario {self.id_user}>'