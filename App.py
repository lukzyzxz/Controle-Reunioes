from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_super_secreta_para_sessoes"  # Necessário para login funcionar

# --------------------- USUÁRIOS ---------------------
Usuarios = {
    "admin": "admin123",
    "bispo": "bispo123",
    "conselheiro1": "cons1",
    "conselheiro2": "cons2",
    "secretario": "secret123"
}

# --------------------- BANCO DE DADOS ---------------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reunioes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    tema TEXT NOT NULL,
                    orador TEXT NOT NULL,
                    observacoes TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --------------------- ROTAS ---------------------
@app.route('/')
def home():
    # Se o usuário estiver logado, vai para a página principal
    if 'usuario' in session:
        return redirect(url_for('painel'))
    return redirect(url_for('login'))

# --------------------- LOGIN ---------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario in Usuarios and Usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('painel'))
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos.")

    return render_template('login.html')

# --------------------- LOGOUT ---------------------
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# --------------------- PÁGINA PRINCIPAL (PAINEL) ---------------------
@app.route('/painel')
def painel():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reunioes ORDER BY data DESC")
    reunioes = c.fetchall()
    conn.close()

    return render_template('index.html', reunioes=reunioes, usuario=session['usuario'])

# --------------------- HISTÓRICO (OPCIONAL) ---------------------
@app.route('/historico')
def historico():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reunioes ORDER BY data DESC")
    reunioes = c.fetchall()
    conn.close()

    # Usa a mesma página principal, só muda o título
    return render_template('index.html', reunioes=reunioes, usuario=session['usuario'])

# --------------------- ADICIONAR REUNIÃO ---------------------
@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    data = request.form['data']
    tema = request.form['tema']
    orador = request.form['orador']
    observacoes = request.form['observacoes']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO reunioes (data, tema, orador, observacoes) VALUES (?, ?, ?, ?)",
              (data, tema, orador, observacoes))
    conn.commit()
    conn.close()

    return redirect(url_for('painel'))
# --------------------- EXECUÇÃO ---------------------
if __name__ == '__main__':
    app.run(debug=True)
