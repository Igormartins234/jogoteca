import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = URL.create(
    drivername='mysql+mysqlconnector',
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME')
)


UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'