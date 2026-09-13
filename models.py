from jogoteca import db


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    biblioteca = db.relationship('Biblioteca', backref='jogo', lazy=True)
    avaliacoes = db.relationship('Avaliacoes', backref='jogo', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.nome


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(8), unique=True, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    biblioteca = db.relationship('Biblioteca', backref='usuario', lazy=True)
    avaliacoes = db.relationship('Avaliacoes', backref='usuario', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.nome


class Biblioteca(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    jogo_id = db.Column(db.Integer, db.ForeignKey('jogos.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='quero_jogar')
    favorito = db.Column(db.Boolean, nullable=False, default=False)
    data_adicionado = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return '<Biblioteca %r>' % self.id


class Avaliacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    jogo_id = db.Column(db.Integer, db.ForeignKey('jogos.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
    data = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return '<Avaliacao %r>' % self.id
