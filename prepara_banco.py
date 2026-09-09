import mysql.connector
from mysql.connector import errorcode

print("Conectando ao banco de dados...")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="igor",
        password="123456"
    )

    print("Conectado com sucesso!")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Existe algo errado com o usuário ou senha.")
    else:
        print(err)

    exit()

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS jogoteca")
cursor.execute("CREATE DATABASE jogoteca")
cursor.execute("USE jogoteca")

TABLES = {}

TABLES['jogos'] = ('''
    CREATE TABLE `jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` varchar(50) NOT NULL,
        `categoria` varchar(40) NOT NULL,
        `console` varchar(20) NOT NULL,
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

TABLES['usuarios'] = ('''
    CREATE TABLE `usuarios` (
        `nome` varchar(20) NOT NULL,
        `nickname` varchar(8) NOT NULL,
        `senha` varchar(100) NOT NULL,
        PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print("Criando tabela {}: ".format(tabela_nome), end='')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Já existe")
        else:
            print(err.msg)
    else:
        print("OK")


usuario_sql = "INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)"
usuarios = [
    ("Lucas", "lucas", "123"),
    ("João", "joao", "321"),
    ("Maria", "maria", "abc"),
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute("SELECT * FROM jogoteca.usuarios")
print("Usuários cadastrados:")
for user in cursor.fetchall():
    print(user[1])

jogos_sql = "INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)"
jogos = [
    ("Tetris", "Puzzle", "Atari"),
    ("God of War", "Hack n Slash", "PS2"), 
    ("Mortal Kombat", "Luta", "PS2"),
    ("Valorant", "FPS", "PC"),
    ("Minecraft", "Sandbox", "PS4"),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute("SELECT * FROM jogoteca.jogos")
print("Jogos cadastrados:")
for jogo in cursor.fetchall():
    print(jogo[1])

