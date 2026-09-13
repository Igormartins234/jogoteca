import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField, TextAreaField, validators


class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormularioBiblioteca(FlaskForm):
    status = SelectField(
        'Status',
        choices=[
            ('quero_jogar', 'Quero jogar'),
            ('jogando', 'Jogando'),
            ('concluido', 'Concluído'),
            ('pausado', 'Pausado'),
            ('abandonado', 'Abandonado')
        ]
    )

    favorito = BooleanField('Favorito')

    salvar = SubmitField('Salvar')


class FormularioAvaliacao(FlaskForm):
    nota = SelectField(
        'Nota',
        choices=[
            ('1', '★'),
            ('2', '★★'),
            ('3', '★★★'),
            ('4', '★★★★'),
            ('5', '★★★★★')
        ],
        coerce=int
    )

    review = TextAreaField(
        'Review',
        validators=[
            validators.Optional(),
            validators.Length(max=1000)
        ]
    )

    publicar = SubmitField('Publicar avaliação')


class FormularioAvaliacao(FlaskForm):
    nota = StringField('Nota', [validators.DataRequired()])
    review = StringField('Review', [validators.DataRequired(), validators.Length(min=1, max=1000)])
    salvar = SubmitField('Publicar avaliação')


class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')


class FormularioCadastro(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=20)])
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    cadastrar = SubmitField('Criar conta')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)

    if arquivo != 'capa_padrao.jpg':
        caminho = os.path.join(app.config['UPLOAD_PATH'], arquivo)

        if os.path.exists(caminho):
            os.remove(caminho)