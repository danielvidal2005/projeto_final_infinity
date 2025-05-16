import sqlite3
import bcrypt


def criar_tabela_usuario():
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTIS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                login TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                nivel_acesso TEXT NOT NULL 
                ativo INTEGER DEFAULT 1   
            )
        ''')
        conn.commit()


def cadastrar_usuario(nome_completo: str, login: str, senha: str, nivel_acesso: str) -> bool:
    try:
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios
                (nome_completo, login, senha_hash, nivel_acesso)
                VALUES (?, ?, ?, ?)
            ''', (nome_completo, login, senha_hash, nivel_acesso))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(F"Erro ao cadastrar usuário: {str(e)}")
        return False
    

def validar_login(login:str, senha:str) -> bool:
    '''Verifica as credenciais do usuário'''
    try:
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT senha_hash FROM usuarios WHERE login = ?', (login,))
            resultado = cursor.fetchone()

        if resultado:
            senha_hash = resultado[0].encode('utf-8')
            return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)
        return False
    
    except Exception as e:
        print(f'Erro ao validar login: {str(e)}')
        return False

