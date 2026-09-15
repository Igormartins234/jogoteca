# 🎮 GameHub

> Uma plataforma para descobrir, organizar, avaliar e compartilhar jogos.

O **GameHub** é uma aplicação web desenvolvida em Flask que permite aos usuários criar uma biblioteca pessoal de jogos, acompanhar seu progresso, marcar favoritos, avaliar jogos e explorar o catálogo da comunidade.

O projeto foi desenvolvido como forma de praticar desenvolvimento web, banco de dados, autenticação, relacionamentos entre tabelas e publicação de aplicações na internet.

---

## ✨ Funcionalidades

### 👤 Usuários

- Cadastro de usuários
- Login e logout
- Senhas protegidas com hash
- Perfil público
- Nickname exclusivo
- Avatar baseado na primeira letra do nome
- Proteção de rotas para usuários não autenticados

### 🎮 Jogos

- Cadastro de jogos
- Categoria
- Console/plataforma
- Página individual do jogo
- Sistema de capas
- Busca por jogos
- Filtro por categoria
- Filtro por console
- Edição de jogos pelo usuário que os criou
- Exclusão de jogos pelo criador

### 📚 Biblioteca

Cada usuário possui sua própria biblioteca.

É possível adicionar jogos com diferentes status:

- 🟠 Quero jogar
- 🔵 Jogando
- 🟢 Concluído
- 🟡 Pausado
- ⚫ Abandonado

Também é possível:

- Marcar jogos como favoritos
- Alterar o status
- Remover jogos da biblioteca
- Visualizar a biblioteca pelo perfil

### ⭐ Avaliações

- Avaliação de jogos
- Nota de 1 a 5
- Review escrita
- Média das avaliações
- Uma avaliação por usuário para cada jogo

### 👥 Comunidade

- Exploração dos jogos cadastrados
- Perfis dos jogadores
- Visualização das bibliotecas
- Visualização dos favoritos
- Jogos criados pelos usuários

---

## 🖥️ Tecnologias

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-WTF
- WTForms

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap
- Jinja2
- SVG

### Banco de dados

- MySQL
- SQLAlchemy
- Aiven MySQL

### Deploy

- Git
- GitHub
- Render

---

## 🗂️ Estrutura do projeto

```text
jogoteca/
│
├── jogoteca.py
├── config.py
├── models.py
├── views_games.py
├── views_user.py
├── helpers.py
├── prepara_banco.py
├── requirements.txt
├── .env
├── .gitignore
│
├── templates/
│   ├── template.html
│   ├── login.html
│   ├── cadastro.html
│   ├── lista.html
│   ├── jogo.html
│   ├── novo.html
│   ├── editar.html
│   ├── biblioteca.html
│   ├── comunidade.html
│   ├── perfil.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
└── uploads/
