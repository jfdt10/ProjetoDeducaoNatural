import google.generativeai as genai
import os
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do arquivo .env

class Gemini:
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configuração da API Key usando variável de ambiente
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida.")
    
    genai.configure(api_key=GOOGLE_API_KEY)

    @staticmethod
    def get_response(prompt: str):
        """Gera uma resposta usando o modelo Gemini."""
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao gerar texto: {e}"

    @staticmethod
    def resolvedor_llm(n_sentencas: str, sentencas: str, problema: str):
        """Resolve um problema de lógica proposicional."""
        prompt = (
            f"Resolva esse problema de lógica apresentado a seguir segundo as regras de lógica proposicional:\n\n"
            f"Número de sentenças que serão apresentadas para você: {n_sentencas}.\n"
            f"Agora, serão mostradas a entrada das sentenças no seguinte formato: 'A: sentença' sendo 'A' a letra que irá "
            f"representar tal sentença no problema e 'sentença' sendo a sentença em linguagem natural.\n"
            f"Sentenças postas pelo usuário: {sentencas}.\n"
            f"Agora, irei te mostrar o problema lógico que quero que resolva a partir do que mostrei: {problema}.\n"
            f"A partir disso quero que me diga a resposta do problema me dizendo como chegou até ela."
        )
        return Gemini.get_response(prompt)

    @staticmethod
    def avaliador_llm(n_sentencas: str, sentencas: str, problema: str, solucao: str):
        """Avalia se a solução de um problema de lógica é válida."""
        prompt = (
            f"Avalie se a solução desse problema de lógica proposicional apresentado a seguir é válida ou não por meio da dedução natural ou das regras de inferência: \n\n"
            f"Número de sentenças que serão apresentadas para você: {n_sentencas}.\n"
            f"Agora, serão mostradas a entrada das sentenças no seguinte formato: 'A: sentença' sendo 'A' a letra que irá "
            f"representar tal sentença no problema e 'sentença' sendo a sentença em linguagem natural.\n"
            f"Sentenças postas pelo usuário: {sentencas}.\n"
            f"Agora, irei te mostrar o problema lógico: {problema}. \n"
            f"E essa é a solução: {solucao}.\n"
            f"A partir disso, quero que me diga se esse problema é válido ou não."
        )
        return Gemini.get_response(prompt)

    @staticmethod
    def tradutor_llm(n_sentencas: str, sentencas: str, solucao: str):
        """Traduz um problema de linguagem natural para lógica proposicional."""
        prompt = (
            f"Traduza o problema a seguir de linguagem natural para a linguagem de lógica proposicional:\n"
            f"Número de sentenças que serão apresentadas para você: {n_sentencas}.\n"
            f"Agora, serão mostradas a entrada das sentenças no seguinte formato: 'A: sentença' sendo 'A' a letra que irá "
            f"representar tal sentença no problema e 'sentença' sendo a sentença em linguagem natural.\n"
            f"Sentenças postas pelo usuário: {sentencas}.\n"
            f"E essa é a solução (se tiver 'N/A' escrito, é porque não há solução, traduza apenas as sentenças do problema): {solucao}.\n"
            f"A partir disso, traduza o problema e me diga quais símbolos equivalem a quais sentenças depois."
        )
        return Gemini.get_response(prompt)
