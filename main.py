import os
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)  # Remove o banco antigo (para testes locais)
    with open('schema.sql', encoding='utf-8') as f:
        conn = sqlite3.connect(DATABASE)
        conn.executescript(f.read())
        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.get_json()
    nome = data.get('nome')
    rua = data.get('rua')
    filhos = data.get('filhos', [])

    if not nome or not rua:
        return jsonify({'erro': 'Nome e rua são obrigatórios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documentos (nome, rua) VALUES (?, ?)", (nome, rua))
    doc_id = cursor.lastrowid

    for filho in filhos:
        cursor.execute("INSERT INTO filhos (documento_id, nome) VALUES (?, ?)", (doc_id, filho.strip()))

    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Documento cadastrado com sucesso'}), 201

@app.route('/pesquisar_nome', methods=['GET'])
def pesquisar_nome():
    nome = request.args.get('nome')
    if not nome:
        return jsonify({'erro': 'Parâmetro "nome" é obrigatório'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documentos WHERE nome = ?", (nome,))
    docs = cursor.fetchall()

    resultados = []
    for doc in docs:
        cursor.execute("SELECT nome FROM filhos WHERE documento_id = ?", (doc['id'],))
        filhos = [f['nome'] for f in cursor.fetchall()]
        resultados.append({
            'id': doc['id'],
            'nome': doc['nome'],
            'rua': doc['rua'],
            'filhos': filhos
        })

    conn.close()
    return jsonify(resultados)

@app.route('/pesquisar_rua', methods=['GET'])
def pesquisar_rua():
    rua = request.args.get('rua')
    if not rua:
        return jsonify({'erro': 'Parâmetro "rua" é obrigatório'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documentos WHERE rua = ?", (rua,))
    docs = cursor.fetchall()

    resultados = []
    for doc in docs:
        cursor.execute("SELECT nome FROM filhos WHERE documento_id = ?", (doc['id'],))
        filhos = [f['nome'] for f in cursor.fetchall()]
        resultados.append({
            'id': doc['id'],
            'nome': doc['nome'],
            'rua': doc['rua'],
            'filhos': filhos
        })

    conn.close()
    return jsonify(resultados)

@app.route('/pesquisar_filhos', methods=['GET'])
def pesquisar_filhos():
    nome_filho = request.args.get('filho')
    if not nome_filho:
        return jsonify({'erro': 'Parâmetro "filho" é obrigatório'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.id, d.nome, d.rua
        FROM documentos d
        JOIN filhos f ON d.id = f.documento_id
        WHERE f.nome = ?
    """, (nome_filho,))
    docs = cursor.fetchall()

    resultados = []
    for doc in docs:
        cursor.execute("SELECT nome FROM filhos WHERE documento_id = ?", (doc['id'],))
        filhos = [f['nome'] for f in cursor.fetchall()]
        resultados.append({
            'id': doc['id'],
            'nome': doc['nome'],
            'rua': doc['rua'],
            'filhos': filhos
        })

    conn.close()
    return jsonify(resultados)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
