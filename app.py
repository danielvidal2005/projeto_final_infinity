from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import usuarios
from autenticacao import login_obrigatorio, acesso_minimo
from inventario import obter_itens_com_imagem, inserir_item

app = Flask(__name__)
app.secret_key = 'top_secret'


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    senha = request.form['senha']

    if usuarios.validar_login(login, senha):
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome_completo, nivel_acesso FROM usuarios WHERE login = ?', (login,))
            user_data = cursor.fetchone()
        
        session['usuario'] = user_data[0]
        session['nivel'] = int(user_data[1])
        return redirect(url_for('painel'))
    else:
        return render_template('login.html', erro="Login inválido")


@app.route('/painel')
@login_obrigatorio
def painel():
    return render_template(
        'index.html',
        nome_usuario=session.get('usuario'),
        nivel_acesso=session.get('nivel'),
        nivel=session.get('nivel')
    )


@app.route('/cadastrar_usuario')
@acesso_minimo(1)  # Apenas nível 1 (Admin)
def cadastrar_usuario():
    return "Página de cadastro de usuários (apenas Admin)"



@app.route('/consultar_itens')
@acesso_minimo(4)
def consultar_itens():
    itens = obter_itens_com_imagem()
    return render_template('consultar_itens.html', itens=itens)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/cadastrar_item', methods=['GET', 'POST'])
@acesso_minimo(3)
def cadastrar_item():
    if request.method == 'POST':
        nome = request.form['item']
        tipo = request.form['tipo']
        quantidade = request.form['quantidade']
        imagem = request.files['imagem']
        caminho_temporario = f"temp_{imagem.filename}"
        imagem.save(caminho_temporario)

        inserir_item(nome, tipo, int(quantidade), caminho_temporario)
        return redirect(url_for('consultar_itens'))

    return render_template('cadastrar_item.html')


if __name__ == '__main__':
    usuarios.criar_tabela_usuario()
    usuarios.criar_admin_padrao()
    app.run(debug=True)
