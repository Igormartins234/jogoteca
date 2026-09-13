from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


from views_games import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)