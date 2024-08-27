import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:lacueva2024@localhost/se_chapinas')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
