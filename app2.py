from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import Gemini
from validar import validar
import re
from graphviz import Digraph
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

def obter_parametros(data, request_method):
    """
    Obtém os parâmetros da requisição, seja POST ou GET.
    """
    if request_method == 'POST':
        return data.get('n_sentencas'), data.get('sentencas'), data.get('problema'), data.get('solucao')
    else:
        return (
            request.args.get('n_sentencas'),
            request.args.get('sentencas'),
            request.args.get('problema'),
            request.args.get('solucao')
        )

@app.route('/resolvedor_llm', methods=['POST', 'GET'])
def resolvedor_llm():
    data = request.get_json() if request.method == 'POST' else {}
    n_sentencas, sentencas, problema, _ = obter_parametros(data, request.method)

    if not n_sentencas or not sentencas or not problema:
        return jsonify({"error": "Parâmetros 'n_sentencas', 'sentencas' e 'problema' são obrigatórios."}), 400

    try:
        resposta = Gemini.resolvedor_llm(n_sentencas, sentencas, problema)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

@app.route('/avaliador_llm', methods=['POST', 'GET'])
def avaliador_llm():
    data = request.get_json() if request.method == 'POST' else {}
    n_sentencas, sentencas, problema, solucao = obter_parametros(data, request.method)

    if not n_sentencas or not sentencas or not problema or not solucao:
        return jsonify({"error": "Parâmetros 'n_sentencas', 'sentencas', 'problema' e 'solucao' são obrigatórios."}), 400

    try:
        resposta = Gemini.avaliador_llm(n_sentencas, sentencas, problema, solucao)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

@app.route('/tradutor_llm', methods=['POST', 'GET'])
def tradutor_llm():
    data = request.get_json() if request.method == 'POST' else {}
    n_sentencas, sentencas, _, solucao = obter_parametros(data, request.method)

    if not n_sentencas or not sentencas or not solucao:
        return jsonify({"error": "Parâmetros 'n_sentencas', 'sentencas' e 'solucao' são obrigatórios."}), 400

    try:
        resposta = Gemini.tradutor_llm(n_sentencas, sentencas, solucao)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

@app.route('/validar_deducao', methods=['POST', 'GET'])
def validar_deducao():
    data = request.get_json() if request.method == 'POST' else {}
    premissas_e_conclusao = data.get('premissas_e_conclusao') if request.method == 'POST' else request.args.get('premissas_e_conclusao')
    passos = data.get('passos') if request.method == 'POST' else request.args.get('passos')

    if not premissas_e_conclusao or not passos:
        return jsonify({"error": "Parâmetros 'premissas_e_conclusao' e 'passos' são obrigatórios."}), 400

    try:
        valido, feedback, caminho_grafo = validar(premissas_e_conclusao, passos)

        premissas = premissas_e_conclusao.split(" ⊢ ")[0].split(", ")
        conclusao = premissas_e_conclusao.split(" ⊢ ")[1]

        feedback_formatado = {
            "premissas": premissas,
            "conclusao": conclusao,
            "passos": passos.strip().split("\n"),
            "feedback": feedback,
            "valido": valido,
            "caminho_grafo": caminho_grafo
        }

        return jsonify(feedback_formatado), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3399)