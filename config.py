import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://{usuario}:{senha}@{servidor}:{porta}/{database}'.format(
        usuario=os.getenv('DB_USER'),
        senha=os.getenv('DB_PASSWORD'),
        servidor=os.getenv('DB_HOST'),
        porta=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'