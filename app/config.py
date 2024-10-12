import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:lacueva2024@localhost/se_chapinas')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuracion uso de Modelos
    USE_MODEL_OPENAI = True
    USE_MODEL_CV = True

    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'none@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'none')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'gon20335@uvg.edu.gt')