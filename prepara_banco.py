import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='igor',
        password='123456',
        charset='utf8mb4',
        collation='utf8mb4_bin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
    exit()

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")
cursor.execute("CREATE DATABASE `jogoteca`;")
cursor.execute("USE `jogoteca`;")

TABLES = {}

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `nickname` (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''')

TABLES['Jogos'] = ('''
      CREATE TABLE `jogos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      `usuario_id` int(11) NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''')

TABLES['Biblioteca'] = ('''
      CREATE TABLE `biblioteca` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `usuario_id` int(11) NOT NULL,
      `jogo_id` int(11) NOT NULL,
      `status` varchar(20) NOT NULL DEFAULT 'quero_jogar',
      `favorito` tinyint(1) NOT NULL DEFAULT 0,
      `data_adicionado` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `usuario_jogo` (`usuario_id`, `jogo_id`),
      FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
      FOREIGN KEY (`jogo_id`) REFERENCES `jogos` (`id`) ON DELETE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''')


TABLES['Avaliacoes'] = ('''
      CREATE TABLE `avaliacoes` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `usuario_id` int(11) NOT NULL,
      `jogo_id` int(11) NOT NULL,
      `nota` int(11) NOT NULL,
      `review` text NULL,
      `data` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `usuario_jogo` (`usuario_id`, `jogo_id`),
      FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
      FOREIGN KEY (`jogo_id`) REFERENCES `jogos` (`id`) ON DELETE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'

usuarios = [
    ("João", "joao", generate_password_hash("321").decode('utf-8')),
    ("Lucas", "lucas", generate_password_hash("123").decode('utf-8')),
    ("Maria", "maria", generate_password_hash("abc").decode('utf-8'))
]

cursor.executemany(usuario_sql, usuarios)

cursor.execute('SELECT * FROM usuarios')

print('------------- Usuários: -------------')

for user in cursor.fetchall():
    print(user[0], user[1], user[2])

jogos_sql = '''
    INSERT INTO jogos (nome, categoria, console, usuario_id)
    VALUES (%s, %s, %s, %s)
'''

jogos = [
    ('Tetris', 'Puzzle', 'Atari', 1),
    ('God of War', 'Ação', 'PS2', 1),
    ('Mortal Kombat', 'Luta', 'PS2', 2),
    ('Valorant', 'FPS', 'PC', 2),
    ('Crash Bandicoot', 'Plataforma', 'PS2', 3),
    ('Need for Speed', 'Corrida', 'PS2', 3),
    ('Minecraft', 'Sandbox', 'PC', 1),
    ('Spider-Man', 'Ação', 'PS5', 2)
]

cursor.executemany(jogos_sql, jogos)

cursor.execute('SELECT * FROM jogos')

print('------------- Jogos: -------------')

for jogo in cursor.fetchall():
    print(jogo[0], jogo[1], jogo[2], jogo[3])

biblioteca_sql = '''
    INSERT INTO biblioteca (usuario_id, jogo_id, status, favorito)
    VALUES (%s, %s, %s, %s)
'''

biblioteca = [
    (jogo[4], jogo[0], 'quero_jogar', 0)
    for jogo in jogos
]

cursor.executemany(biblioteca_sql, biblioteca)

cursor.execute('''
    SELECT
        usuarios.nickname,
        jogos.nome,
        biblioteca.status,
        biblioteca.favorito
    FROM biblioteca
    INNER JOIN usuarios ON usuarios.id = biblioteca.usuario_id
    INNER JOIN jogos ON jogos.id = biblioteca.jogo_id
    ORDER BY biblioteca.id
''')

print('------------- Bibliotecas: -------------')

for item in cursor.fetchall():
    favorito = 'Sim' if item[3] else 'Não'
    print(item[0], '|', item[1], '|', item[2], '| Favorito:', favorito)

conn.commit()

cursor.close()
conn.close()

print('Banco criado com sucesso!')