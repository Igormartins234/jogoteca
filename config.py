import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'