SECRET_KEY = 'alohomora'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'igor',
        senha = '123456',
        servidor = 'localhost',  
        database = 'jogoteca'
    )
