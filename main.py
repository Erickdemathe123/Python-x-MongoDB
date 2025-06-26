from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Conexão com o MongoDB (ajuste se necessário)
client = MongoClient("mongodb://localhost:27017/")
db = client["cadastroDB"]
collection = db["documentos"]

# Rota para cadastrar documento
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados ausentes"}), 400
    collection.insert_one(dados)
    return jsonify({"mensagem": "Documento cadastrado com sucesso!"}), 201

# Rota para pesquisar por nome
@app.route("/pesquisar_nome", methods=["GET"])
def pesquisar_nome():
    nome = request.args.get("nome")
    resultados = list(collection.find({"nome": nome}, {"_id": 0}))
    return jsonify(resultados)

# Rota para pesquisar por rua
@app.route("/pesquisar_rua", methods=["GET"])
def pesquisar_rua():
    rua = request.args.get("rua")
    resultados = list(collection.find({"endereco.rua": rua}, {"_id": 0}))
    return jsonify(resultados)

# Rota para pesquisar por filhos
@app.route("/pesquisar_filhos", methods=["GET"])
def pesquisar_filhos():
    filho = request.args.get("filho")
    resultados = list(collection.find({"filhos": filho}, {"_id": 0}))
    return jsonify(resultados)

# Rota principal
@app.route("/")
def index():
    return "API Python x MongoDB ativa!"

if __name__ == "__main__":
    app.run(debug=True)
