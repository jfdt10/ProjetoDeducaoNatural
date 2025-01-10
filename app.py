from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import Gemini
from validar import validar
import re
from graphviz import Digraph
import os


app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Endpoint para resolver um problema de lógica usando o Gemini
@app.route('/resolvedor_llm', methods=['POST'])
def resolvedor_llm():
    """
    Endpoint para resolver um problema de lógica.
    Recebe JSON com 'n_sentencas', 'sentencas' e 'problema'.
    Retorna a solução gerada pelo Gemini.
    """
    data = request.get_json()
    n_sentencas = data.get('n_sentencas')
    sentencas = data.get('sentencas')
    problema = data.get('problema')

    if not n_sentencas or not sentencas or not problema:
        return jsonify({"error": "Parâmetros 'n_sentencas', 'sentencas' e 'problema' são obrigatórios."}), 400

    try:
        resposta = Gemini.resolvedor_llm(n_sentencas, sentencas, problema)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

# Endpoint para avaliar uma solução de um problema de lógica usando o Gemini
@app.route('/avaliador_llm', methods=['POST'])
def avaliador_llm():
    """
    Endpoint para avaliar uma solução de um problema de lógica.
    Recebe JSON com 'n_sentencas', 'sentencas', 'problema' e 'solucao'.
    Retorna a avaliação gerada pelo Gemini.
    """
    data = request.get_json()
    n_sentencas = data.get('n_sentencas')
    sentencas = data.get('sentencas')
    problema = data.get('problema')
    solucao = data.get('solucao')

    if not n_sentencas or not sentencas or not problema or not solucao:
        return jsonify({"error": "Parâmetros 'n_sentencas', 'sentencas', 'problema' e 'solucao' são obrigatórios."}), 400

    try:
        resposta = Gemini.avaliador_llm(n_sentencas, sentencas, problema, solucao)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

# Endpoint para traduzir um problema de linguagem natural para lógica proposicional usando o Gemini
@app.route('/tradutor_llm', methods=['POST'])
def tradutor_llm():
    """
    Endpoint para traduzir um problema de linguagem natural para lógica proposicional.
    Recebe JSON com 'n_sentencas', 'sentencas' e 'solucao'.
    Retorna a tradução gerada pelo Gemini.
    """
    data = request.get_json()
    n_sentencas = data.get('n_sentencas')
    sentencas = data.get('sentencas')
    solucao = data.get('solucao')

    if not n_sentencas or not sentencas or not solucao:
        return jsonify({"error": "Parâmetros 'n_sentencas', 'sentencas' e 'solucao' são obrigatórios."}), 400

    try:
        resposta = Gemini.tradutor_llm(n_sentencas, sentencas, solucao)
        return jsonify({"resposta": resposta}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

# Endpoint para validar uma dedução lógica
@app.route('/validar_deducao', methods=['POST'])
def validar_deducao():
    data = request.get_json()
    premissas_e_conclusao = data.get('premissas_e_conclusao')
    passos = data.get('passos')

    if not premissas_e_conclusao or not passos:
        return jsonify({"error": "Parâmetros 'premissas_e_conclusao' e 'passos' são obrigatórios."}), 400

    try:
        # Chama a função validar
        valido, feedback, caminho_grafo = validar(premissas_e_conclusao, passos)

        # Separa as premissas e a conclusão
        premissas = premissas_e_conclusao.split(" ⊢ ")[0].split(", ")
        conclusao = premissas_e_conclusao.split(" ⊢ ")[1]

        # Formata o feedback para incluir premissas, conclusão e passos
        feedback_formatado = {
            "premissas": premissas,
            "conclusao": conclusao,
            "passos": passos.strip().split("\n"),
            "feedback": feedback,
            "valido": valido,
            "caminho_grafo": caminho_grafo  # Já está no formato SVG
        }

        return jsonify(feedback_formatado), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao processar a solicitação: {str(e)}"}), 500

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3399)
