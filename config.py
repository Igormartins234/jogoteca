import os

SECRET_KEY = 'ruass'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'igor',
        senha = '123456',
        servidor = 'localhost',
        database = 'jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'