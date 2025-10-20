from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_super_secreta_para_sessoes"

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
                    dirigente TEXT,
                    orador TEXT,
                    hino_inicial TEXT,
                    hino_sacramental TEXT,
                    hino_final TEXT,
                    oracao_inicial TEXT,
                    oracao_final TEXT,
                    membros_presentes INTEGER,
                    observacoes TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --------------------- ROTAS ---------------------
@app.route('/')
def home():
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

# --------------------- PAINEL PRINCIPAL ---------------------
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

# --------------------- ADICIONAR REUNIÃO ---------------------
@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    dados = (
        request.form['data'],
        request.form['tema'],
        request.form['dirigente'],
        request.form['orador'],
        request.form['hino_inicial'],
        request.form['hino_sacramental'],
        request.form['hino_final'],
        request.form['oracao_inicial'],
        request.form['oracao_final'],
        request.form['membros_presentes'],
        request.form['observacoes']
    )

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO reunioes 
                 (data, tema, dirigente, orador, hino_inicial, hino_sacramental, hino_final,
                  oracao_inicial, oracao_final, membros_presentes, observacoes)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', dados)
    conn.commit()
    conn.close()

    return redirect(url_for('painel'))

# --------------------- HISTÓRICO ---------------------
@app.route('/historico')
def historico():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reunioes ORDER BY data DESC")
    reunioes = c.fetchall()
    conn.close()

    return render_template('historico.html', reunioes=reunioes, usuario=session['usuario'])

# --------------------- EXECUÇÃO ---------------------
if __name__ == '__main__':
    app.run(debug=True)
