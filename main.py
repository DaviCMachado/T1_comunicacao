


import matplotlib.pyplot as plt


# Bora lá gurizada
#  Fazer esse trabalho com o coração


# TRABALHO TEÓRICO 
# Trabalho teórico: texto escrito descrevendo 3 códigos de
# linha que não tenham sido estudados em aula contendo:

# • Introdução sobre códigos de linha
# • Explicação sobre o primeiro padrão de código de linha
# • Explicação sobre o segundo padrão de código de linha
# • Explicação sobre o terceiro padrão de código de linha
# • Conclusão

# TRABALHO PRÁTICO
# • Implementar um sistema de visualização para os códigos de linha
# apresentados em aula (NRZ-I, NRZ-L, AMI, Pseudoternário,
# Manchester, Mancherter Diferencial bem como os 3 escolhidos no
# trabalho teórico)
# • O usuário deve ser capaz de escolher um dos códigos de
# linha e entrar com a sequência de bits a ser visualizada


# Passo 1: definir os 3 codigos de linha 

# Passo 2: criar a funcao de codificacao
# 
# def codificacao(codigo, bits):
#     if codigo == "NRZ-I":
#         return nrzi(bits)
#     elif codigo == "NRZ-L":
#         return nrzl(bits)
#     elif codigo == "AMI":
#         return ami(bits)
#     elif codigo == "Pseudoternário":
#         return pseudoternario(bits)
#    elif codigo == "Manchester":
#        return manchester(bits)
#    elif codigo == "Manchester Diferencial":
#       return manchester_diferencial(bits)
#    elif codigo == "Codigo 1":
#       return codigo1(bits)
#    elif codigo == "Codigo 2":
#      return codigo2(bits)
#   elif codigo == "Codigo 3":
#     return codigo3(bits)
# Passo 3: criar a funcao de decodificacao
# def decodificacao(codigo, bits):
#    if codigo == "NRZ-I":
#       return nrzi(bits)
#   elif codigo == "NRZ-L":
#      return nrzl(bits)
#   elif codigo == "AMI":
#      return ami(bits)
#  elif codigo == "Pseudoternário":
#     return pseudoternario(bits)
#   elif codigo == "Manchester":
#     return manchester(bits)
#  elif codigo == "Manchester Diferencial":
#   return manchester_diferencial(bits)
#  elif codigo == "Codigo 1":
#    return codigo1(bits)
#  elif codigo == "Codigo 2":
#   return codigo2(bits)
# elif codigo == "Codigo 3":
#  return codigo3(bits)
# Passo 4: criar a funcao de plotagem
# def plotar(codigo, bits):
#   if codigo == "NRZ-I":
#     return nrzi(bits)
#  elif codigo == "NRZ-L":
#    return nrzl(bits)
# elif codigo == "AMI":
#   return ami(bits)
# elif codigo == "Pseudoternário":
#  return pseudoternario(bits)
# elif codigo == "Manchester":
#  

# Passo 4: criar as funcoes de codificacao de linha

# Passo 5: plotar graficos


# Função para NRZ-L
def nrzl(bits):
    sinal = []
    tempo = []

    nivel = 1  # nível inicial arbitrário

    for i, bit in enumerate(bits):
        if bit == '1':
            nivel = 1
        else:
            nivel = -1
        sinal.extend([nivel, nivel])
        tempo.extend([i, i + 1])

    return tempo, sinal

# Função para plotar o sinal
def plotar(tempo, sinal, titulo="Codificação de Linha"):
    plt.figure(figsize=(10, 3))
    plt.title(titulo)
    plt.xlabel("Tempo")
    plt.ylabel("Nível")
    plt.grid(True)
    plt.plot(tempo, sinal, drawstyle='steps-post')
    plt.ylim(-2, 2)
    plt.yticks([-1, 0, 1])
    plt.show()


def menu():
    print("=== Visualizador de Códigos de Linha ===")
    print("Opções disponíveis:")
    codigos = ["NRZ-L"]
    for i, nome in enumerate(codigos):
        print(f"{i + 1}. {nome}")

    escolha = int(input("Escolha o código de linha (número): ")) - 1
    if escolha < 0 or escolha >= len(codigos):
        print("Escolha inválida.")
        return

    bits = input("Digite a sequência de bits: ")
    if not all(b in '01' for b in bits):
        print("Sequência inválida. Use apenas 0 e 1.")
        return

    codigo = codigos[escolha]
    
    if codigo == "NRZ-L":
        tempo, sinal = nrzl(bits)
        plotar(tempo, sinal, titulo=f"Codificação {codigo}")

# Função principal
def main():
    while True:
        menu()
        continuar = input("Deseja continuar? (s/n): ").strip().lower()
        if continuar != 's':
            break



if __name__ == "__main__":
    main()
