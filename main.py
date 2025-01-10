from gemini import Gemini

def coletar_entrada(mensagem):
    """Coleta múltiplas linhas de entrada do usuário."""
    print(mensagem)
    linhas = []
    while True:
        try:
            linha = input()
            if linha.strip(): 
                linhas.append(linha)
        except EOFError: 
            break
    return "\n".join(linhas)

def resolvedor_llm(n_sentencas=None, sentencas=None, problema=None):
    """Função para resolver um problema de lógica."""
    if n_sentencas is None:
        n_sentencas = input("Digite o número de sentenças que existem no seu problema: ")
        if not n_sentencas.isdigit():
            print("Erro: O número de sentenças deve ser um valor inteiro.")
            return None

    if sentencas is None:
        sentencas = coletar_entrada("\nDigite as sentenças (pressione Enter após cada linha e Ctrl+D para finalizar):\nEx:\nA: Chuva\nB: Rua Molhada\nC: Rua Escorregadia\n")

    if problema is None:
        problema = coletar_entrada("\nDigite o problema utilizando quebra de linha para separar cada sentença e o número da mesma na frente (pressione Enter após cada linha e Ctrl+D para finalizar):\nEx:\n1-A → B\n2-B → C\n3-A\n")

    return Gemini.resolvedor_llm(n_sentencas, sentencas, problema)

def avaliador_llm(n_sentencas=None, sentencas=None, problema=None, solucao=None):
    """Função para avaliar uma solução de um problema de lógica."""
    if n_sentencas is None:
        n_sentencas = input("Digite o número de sentenças que existem no seu problema: ")
        if not n_sentencas.isdigit():
            print("Erro: O número de sentenças deve ser um valor inteiro.")
            return None

    if sentencas is None:
        sentencas = coletar_entrada("\nDigite as sentenças (pressione Enter após cada linha e Ctrl+D para finalizar):\nEx:\nA: Chuva\nB: Rua Molhada\nC: Rua Escorregadia\n")

    if problema is None:
        problema = coletar_entrada("\nDigite o problema utilizando quebra de linha para separar cada sentença e o número da mesma na frente (pressione Enter após cada linha e Ctrl+D para finalizar):\nEx:\n1-A → B\n2-B → C\n3-A\n")

    if solucao is None:
        solucao = coletar_entrada("\nDigite a resposta do problema (pressione Enter após cada linha e Ctrl+D para finalizar):\n")

    return Gemini.avaliador_llm(n_sentencas, sentencas, problema, solucao)

def tradutor_llm(n_sentencas=None, sentencas=None, solucao=None):
    """Função para traduzir um problema de linguagem natural para lógica proposicional."""
    if n_sentencas is None:
        n_sentencas = input("Digite o número de sentenças que existem no seu problema: ")
        if not n_sentencas.isdigit():
            print("Erro: O número de sentenças deve ser um valor inteiro.")
            return None

    if sentencas is None:
        sentencas = coletar_entrada("\nDigite o problema utilizando quebra de linha para separar cada sentença e o número da mesma na frente (pressione Enter após cada linha e Ctrl+D para finalizar):\nEx:\n1.Se Ana for promovida, então Bruno não será promovido.\n2.Se Carlos for promovido, então Ana também será promovida.\n3.Bruno será promovido se, e somente se, Carlos não for promovido.\n")

    if solucao is None:
        solucao = coletar_entrada("\nDigite a resposta do problema (pressione Enter após cada linha e Ctrl+D para finalizar):\n")

    return Gemini.tradutor_llm(n_sentencas, sentencas, solucao)

def main():
    """Função principal do programa."""
    while True:
        operacao = input("\nQual operação será feita? \n1. Resolvedor \n2. Avaliador \n3. Tradutor \n4. Sair\nEscolha uma opção: ")

        if operacao == "1":
            resposta = resolvedor_llm()
            if resposta:
                print("\nResposta do resolvedor:")
                print(resposta)
        elif operacao == "2":
            resposta = avaliador_llm()
            if resposta:
                print("\nResposta do avaliador:")
                print(resposta)
        elif operacao == "3":
            resposta = tradutor_llm()
            if resposta:
                print("\nResposta do tradutor:")
                print(resposta)
        elif operacao == "4":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
