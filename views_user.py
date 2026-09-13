from jogoteca import app, db
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios, Biblioteca, Avaliacoes
from helpers import FormularioUsuario, FormularioCadastro
from flask_bcrypt import check_password_hash, generate_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    if usuario and check_password_hash(usuario.senha, form.senha.data):
        session['usuario_logado'] = usuario.nickname
        session['usuario_id'] = usuario.id

        flash(usuario.nickname + ' logado com sucesso!')

        proxima_pagina = request.form.get('proxima')

        if proxima_pagina:
            return redirect(proxima_pagina)

        return redirect(url_for('index'))

    flash('Usuário não logado.')
    return redirect(url_for('login'))


@app.route('/cadastro')
def cadastro():
    form = FormularioCadastro()
    return render_template('cadastro.html', form=form)


@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    form = FormularioCadastro(request.form)

    if not form.validate():
        flash('Preencha os campos corretamente.')
        return redirect(url_for('cadastro'))

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    if usuario:
        flash('Esse nickname já está cadastrado.')
        return redirect(url_for('cadastro'))

    senha = generate_password_hash(form.senha.data).decode('utf-8')

    novo_usuario = Usuarios(
        nickname=form.nickname.data,
        nome=form.nome.data,
        senha=senha
    )

    db.session.add(novo_usuario)
    db.session.commit()

    flash('Conta criada com sucesso! Faça login para continuar.')

    return redirect(url_for('login'))


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


@app.route('/perfil/<nickname>')
def perfil(nickname):
    usuario = Usuarios.query.filter_by(nickname=nickname).first_or_404()

    biblioteca = Biblioteca.query.filter_by(
        usuario_id=usuario.id
    ).order_by(
        Biblioteca.id.desc()
    ).all()

    favoritos = Biblioteca.query.filter_by(
        usuario_id=usuario.id,
        favorito=True
    ).all()

    concluidos = Biblioteca.query.filter_by(
        usuario_id=usuario.id,
        status='concluido'
    ).count()

    return render_template(
        'perfil.html',
        titulo=usuario.nome,
        usuario=usuario,
        biblioteca=biblioteca,
        favoritos=favoritos,
        concluidos=concluidos
    )



@app.route('/logout')
def logout():
    session.clear()

    flash('Logout efetuado com sucesso!')

    return redirect(url_for('login'))