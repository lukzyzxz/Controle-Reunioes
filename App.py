from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- CRIAR BANCO ----------
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS reunioes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                presidida TEXT,
                dirigida TEXT,
                regente TEXT,
                pianista TEXT,
                anuncios TEXT,
                primeira_oracao TEXT,
                ultima_oracao TEXT,
                hino_inicial TEXT,
                hino_sacramental TEXT,
                hino_especial TEXT,
                hino_intermediario TEXT,
                hino_final TEXT,
                oradores TEXT,
                observacoes TEXT
            )
        """)
        conn.commit()

# ---------- ROTA PRINCIPAL ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dados = (
            request.form.get("data"),
            request.form.get("presidida"),
            request.form.get("dirigida"),
            request.form.get("regente"),
            request.form.get("pianista"),
            request.form.get("anuncios"),
            request.form.get("primeira_oracao"),
            request.form.get("ultima_oracao"),
            request.form.get("hino_inicial"),
            request.form.get("hino_sacramental"),
            request.form.get("hino_especial"),
            request.form.get("hino_intermediario"),
            request.form.get("hino_final"),
            request.form.get("oradores"),
            request.form.get("observacoes")
        )

        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO reunioes (
                    data, presidida, dirigida, regente, pianista, anuncios,
                    primeira_oracao, ultima_oracao, hino_inicial, hino_sacramental,
                    hino_especial, hino_intermediario, hino_final, oradores, observacoes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados)
            conn.commit()

        return redirect(url_for("historico"))

    return render_template("index.html")

# ---------- ROTA HISTÓRICO ----------
@app.route("/historico")
def historico():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM reunioes ORDER BY data DESC")
        reunioes = c.fetchall()
    return render_template("historico.html", reunioes=reunioes)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
