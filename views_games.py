from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Biblioteca, Avaliacoes
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo, FormularioBiblioteca, FormularioAvaliacao
import time


@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    biblioteca = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id']
    ).order_by(
        Biblioteca.id.desc()
    ).all()

    capas_biblioteca = {}

    for item in biblioteca:
        capas_biblioteca[item.jogo_id] = recupera_imagem(item.jogo_id)

    return render_template(
        'lista.html',
        titulo='Minha Biblioteca',
        biblioteca=biblioteca,
        capas_biblioteca=capas_biblioteca
    )


@app.route('/explorar')
def explorar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    busca = request.args.get('q', '')
    categoria = request.args.get('categoria', '')
    console = request.args.get('console', '')

    consulta = Jogos.query

    if busca:
        consulta = consulta.filter(
            Jogos.nome.ilike(f'%{busca}%')
        )

    if categoria:
        consulta = consulta.filter_by(
            categoria=categoria
        )

    if console:
        consulta = consulta.filter_by(
            console=console
        )

    jogos = consulta.order_by(Jogos.nome).all()

    categorias = db.session.query(
        Jogos.categoria
    ).distinct().order_by(Jogos.categoria).all()

    consoles = db.session.query(
        Jogos.console
    ).distinct().order_by(Jogos.console).all()

    return render_template(
        'explorar.html',
        titulo='Explorar',
        jogos=jogos,
        categorias=[categoria[0] for categoria in categorias],
        consoles=[console[0] for console in consoles],
        busca=busca,
        categoria_selecionada=categoria,
        console_selecionado=console
    )


@app.route('/comunidade')
def comunidade():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    biblioteca = Biblioteca.query.order_by(
        Biblioteca.data_adicionado.desc()
    ).all()

    avaliacoes = Avaliacoes.query.order_by(
        Avaliacoes.data.desc()
    ).all()

    atividades = []

    for item in biblioteca:
        atividades.append({
            'tipo': 'biblioteca',
            'data': item.data_adicionado,
            'usuario': item.usuario,
            'jogo': item.jogo,
            'item': item
        })

    for avaliacao in avaliacoes:
        atividades.append({
            'tipo': 'avaliacao',
            'data': avaliacao.data,
            'usuario': avaliacao.usuario,
            'jogo': avaliacao.jogo,
            'avaliacao': avaliacao
        })

    atividades.sort(
        key=lambda atividade: atividade['data'],
        reverse=True
    )

    return render_template(
        'comunidade.html',
        titulo='Comunidade',
        atividades=atividades
    )

@app.route('/novo')
def novo():
    if 'usuario_id' not in session:
        return redirect(url_for('login', proxima=url_for('novo')))

    form = FormularioJogo()

    return render_template(
        'novo.html',
        titulo='Adicionar Jogo',
        form=form
    )


@app.route('/criar', methods=['POST'])
def criar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash('Preencha os campos corretamente.')
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(
        nome=nome
    ).first()

    if jogo:
        flash('Esse jogo já está no catálogo!')
        return redirect(url_for('jogo', id=jogo.id))

    novo_jogo = Jogos(
        nome=nome,
        categoria=categoria,
        console=console
    )

    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files.get('arquivo')

    if arquivo and arquivo.filename:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()

        arquivo.save(
            f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg'
        )

    flash('Jogo adicionado ao catálogo!')

    return redirect(url_for('jogo', id=novo_jogo.id))


@app.route('/jogo/<int:id>')
def jogo(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    jogo = Jogos.query.get_or_404(id)

    biblioteca = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id'],
        jogo_id=id
    ).first()

    avaliacoes = Avaliacoes.query.filter_by(
        jogo_id=id
    ).order_by(
        Avaliacoes.id.desc()
    ).all()

    media = 0

    if avaliacoes:
        media = sum(
            avaliacao.nota for avaliacao in avaliacoes
        ) / len(avaliacoes)

    minha_avaliacao = Avaliacoes.query.filter_by(
        usuario_id=session['usuario_id'],
        jogo_id=id
    ).first()

    quantidade_jogadores = Biblioteca.query.filter_by(
        jogo_id=id
    ).count()

    form_biblioteca = FormularioBiblioteca()
    form_avaliacao = FormularioAvaliacao()

    if biblioteca:
        form_biblioteca.status.data = biblioteca.status
        form_biblioteca.favorito.data = biblioteca.favorito

    if minha_avaliacao:
        form_avaliacao.nota.data = minha_avaliacao.nota
        form_avaliacao.review.data = minha_avaliacao.review

    capa_jogo = recupera_imagem(id)

    return render_template(
        'jogo.html',
        titulo=jogo.nome,
        jogo=jogo,
        biblioteca=biblioteca,
        avaliacoes=avaliacoes,
        media=media,
        minha_avaliacao=minha_avaliacao,
        quantidade_jogadores=quantidade_jogadores,
        form_biblioteca=form_biblioteca,
        form_avaliacao=form_avaliacao,
        capa_jogo=capa_jogo
    )

@app.route('/jogo/<int:id>/avaliar', methods=['POST'])
def avaliar(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    jogo = Jogos.query.get_or_404(id)

    form = FormularioAvaliacao(request.form)

    if not form.validate_on_submit():
        flash('Não foi possível publicar a avaliação.')
        return redirect(url_for('jogo', id=id))

    avaliacao = Avaliacoes.query.filter_by(
        usuario_id=session['usuario_id'],
        jogo_id=id
    ).first()

    if avaliacao:
        avaliacao.nota = form.nota.data
        avaliacao.review = form.review.data
        flash('Sua avaliação foi atualizada.')

    else:
        nova_avaliacao = Avaliacoes(
            usuario_id=session['usuario_id'],
            jogo_id=id,
            nota=form.nota.data,
            review=form.review.data
        )

        db.session.add(nova_avaliacao)

        flash('Avaliação publicada com sucesso.')

    db.session.commit()

    return redirect(url_for('jogo', id=id))

@app.route('/jogo/<int:id>/excluir-avaliacao', methods=['POST'])
def excluir_avaliacao(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    avaliacao = Avaliacoes.query.filter_by(
        id=id,
        usuario_id=session['usuario_id']
    ).first_or_404()

    jogo_id = avaliacao.jogo_id

    db.session.delete(avaliacao)
    db.session.commit()

    flash('Sua avaliação foi excluída.')

    return redirect(url_for('jogo', id=jogo_id))


@app.route('/biblioteca/adicionar/<int:id>', methods=['POST'])
def adicionar_biblioteca(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    jogo = Jogos.query.get_or_404(id)

    existente = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id'],
        jogo_id=jogo.id
    ).first()

    if existente:
        flash('Esse jogo já está na sua biblioteca!')
        return redirect(url_for('jogo', id=id))

    biblioteca = Biblioteca(
        usuario_id=session['usuario_id'],
        jogo_id=jogo.id,
        status='quero_jogar',
        favorito=False
    )

    db.session.add(biblioteca)
    db.session.commit()

    flash('Jogo adicionado à sua biblioteca!')

    return redirect(url_for('jogo', id=id))


@app.route('/biblioteca/remover/<int:id>', methods=['POST'])
def remover_biblioteca(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    biblioteca = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id'],
        jogo_id=id
    ).first()

    if not biblioteca:
        flash('Esse jogo não está na sua biblioteca!')
        return redirect(url_for('jogo', id=id))

    db.session.delete(biblioteca)
    db.session.commit()

    flash('Jogo removido da sua biblioteca!')

    return redirect(url_for('jogo', id=id))


@app.route('/biblioteca/editar/<int:id>', methods=['POST'])
def editar_biblioteca(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    biblioteca = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id'],
        jogo_id=id
    ).first()

    if not biblioteca:
        flash('Esse jogo não está na sua biblioteca!')
        return redirect(url_for('jogo', id=id))

    form = FormularioBiblioteca(request.form)

    if form.validate_on_submit():
        biblioteca.status = form.status.data
        biblioteca.favorito = form.favorito.data

        db.session.commit()

        flash('Biblioteca atualizada com sucesso!')

    return redirect(url_for('jogo', id=id))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.get_or_404(id)

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)

    return render_template(
        'editar.html',
        titulo='Editando Jogo',
        id=id,
        capa_jogo=capa_jogo,
        form=form
    )


@app.route('/atualizar', methods=['POST'])
def atualizar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash('Preencha os campos corretamente.')
        return redirect(url_for('editar', id=request.form['id']))

    jogo = Jogos.query.get(request.form['id'])

    if not jogo:
        flash('Jogo não encontrado!')
        return redirect(url_for('index'))

    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data

    db.session.commit()

    arquivo = request.files.get('arquivo')

    if arquivo and arquivo.filename:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()

        deleta_arquivo(jogo.id)

        arquivo.save(
            f'{upload_path}/capa{jogo.id}-{timestamp}.jpg'
        )

    flash('Jogo atualizado com sucesso!')

    return redirect(url_for('jogo', id=jogo.id))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    jogo = Jogos.query.get_or_404(id)

    biblioteca = Biblioteca.query.filter_by(
        jogo_id=id
    ).all()

    for item in biblioteca:
        db.session.delete(item)

    avaliacoes = Avaliacoes.query.filter_by(
        jogo_id=id
    ).all()

    for avaliacao in avaliacoes:
        db.session.delete(avaliacao)

    deleta_arquivo(id)

    db.session.delete(jogo)
    db.session.commit()

    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/biblioteca')
def biblioteca():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    status = request.args.get('status')
    favoritos = request.args.get('favoritos')

    consulta = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id']
    )

    if status:
        consulta = consulta.filter_by(status=status)

    if favoritos == '1':
        consulta = consulta.filter_by(favorito=True)

    itens = consulta.order_by(
        Biblioteca.id.desc()
    ).all()

    capas_biblioteca = {}

    for item in itens:
        capas_biblioteca[item.jogo_id] = recupera_imagem(item.jogo_id)

    return render_template(
        'biblioteca.html',
        titulo='Minha Biblioteca',
        biblioteca=itens,
        status_atual=status,
        favoritos=favoritos,
        capas_biblioteca=capas_biblioteca
    )

@app.route('/diario')
def diario():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    biblioteca = Biblioteca.query.filter_by(
        usuario_id=session['usuario_id']
    ).order_by(
        Biblioteca.data_adicionado.desc()
    ).all()

    avaliacoes = Avaliacoes.query.filter_by(
        usuario_id=session['usuario_id']
    ).order_by(
        Avaliacoes.data.desc()
    ).all()

    atividades = []

    for item in biblioteca:
        atividades.append({
            'tipo': 'biblioteca',
            'data': item.data_adicionado,
            'jogo': item.jogo,
            'item': item
        })

    for avaliacao in avaliacoes:
        atividades.append({
            'tipo': 'avaliacao',
            'data': avaliacao.data,
            'jogo': avaliacao.jogo,
            'avaliacao': avaliacao
        })

    atividades.sort(
        key=lambda atividade: atividade['data'],
        reverse=True
    )

    return render_template(
        'diario.html',
        titulo='Meu Diário',
        atividades=atividades
    )

@app.route('/estatisticas')
def estatisticas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']

    total_jogos = Biblioteca.query.filter_by(
        usuario_id=usuario_id
    ).count()

    concluidos = Biblioteca.query.filter_by(
        usuario_id=usuario_id,
        status='concluido'
    ).count()

    jogando = Biblioteca.query.filter_by(
        usuario_id=usuario_id,
        status='jogando'
    ).count()

    quero_jogar = Biblioteca.query.filter_by(
        usuario_id=usuario_id,
        status='quero_jogar'
    ).count()

    pausados = Biblioteca.query.filter_by(
        usuario_id=usuario_id,
        status='pausado'
    ).count()

    abandonados = Biblioteca.query.filter_by(
        usuario_id=usuario_id,
        status='abandonado'
    ).count()

    favoritos = Biblioteca.query.filter_by(
        usuario_id=usuario_id,
        favorito=True
    ).count()

    avaliacoes = Avaliacoes.query.filter_by(
        usuario_id=usuario_id
    ).all()

    total_avaliacoes = len(avaliacoes)

    if total_avaliacoes > 0:
        nota_media = sum(
            avaliacao.nota for avaliacao in avaliacoes
        ) / total_avaliacoes
    else:
        nota_media = 0

    jogos_por_console = db.session.query(
        Jogos.console,
        db.func.count(Biblioteca.id)
    ).join(
        Biblioteca,
        Biblioteca.jogo_id == Jogos.id
    ).filter(
        Biblioteca.usuario_id == usuario_id
    ).group_by(
        Jogos.console
    ).order_by(
        db.func.count(Biblioteca.id).desc()
    ).all()

    jogos_por_categoria = db.session.query(
        Jogos.categoria,
        db.func.count(Biblioteca.id)
    ).join(
        Biblioteca,
        Biblioteca.jogo_id == Jogos.id
    ).filter(
        Biblioteca.usuario_id == usuario_id
    ).group_by(
        Jogos.categoria
    ).order_by(
        db.func.count(Biblioteca.id).desc()
    ).all()

    return render_template(
        'estatisticas.html',
        titulo='Minhas Estatísticas',
        total_jogos=total_jogos,
        concluidos=concluidos,
        jogando=jogando,
        quero_jogar=quero_jogar,
        pausados=pausados,
        abandonados=abandonados,
        favoritos=favoritos,
        total_avaliacoes=total_avaliacoes,
        nota_media=nota_media,
        jogos_por_console=jogos_por_console,
        jogos_por_categoria=jogos_por_categoria
    )



@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory(
        app.config['UPLOAD_PATH'],
        nome_arquivo
    )

