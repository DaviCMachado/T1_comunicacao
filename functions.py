# --- Codificações disponíveis ---

def nrzl(bits):
    tempo, sinal = [], []
    t = 0
    for bit in bits:
        tempo += [t, t + 1]
        sinal += [1 if bit == '1' else -1] * 2
        t += 1
    return tempo, sinal

def nrzi(bits):
    tempo, sinal = [], []
    nivel = 1
    t = 0
    for bit in bits:
        if bit == '1':
            nivel *= -1
        tempo += [t, t + 1]
        sinal += [nivel] * 2
        t += 1
    return tempo, sinal

def ami(bits):
    tempo, sinal = [], []
    nivel = 1
    t = 0
    for bit in bits:
        tempo += [t, t + 1]
        if bit == '1':
            sinal += [nivel] * 2
            nivel *= -1
        else:
            sinal += [0] * 2
        t += 1
    return tempo, sinal

def pseudoternario(bits):
    tempo, sinal = [], []
    nivel = 1
    t = 0
    for bit in bits:
        tempo += [t, t + 1]
        if bit == '0':
            sinal += [nivel] * 2
            nivel *= -1
        else:
            sinal += [0] * 2
        t += 1
    return tempo, sinal

def manchester(bits):
    tempo, sinal = [], []
    t = 0
    for bit in bits:
        tempo += [t, t + 0.5, t + 0.5, t + 1]
        if bit == '1':
            sinal += [-1, -1, 1, 1]
        else:
            sinal += [1, 1, -1, -1]
        t += 1
    return tempo, sinal

def manchester_diferencial(bits):
    tempo, sinal = [], []
    nivel = 1
    t = 0
    for bit in bits:
        tempo += [t, t + 0.5, t + 0.5, t + 1]
        if bit == '1':
            nivel *= -1
        sinal += [nivel, nivel, -nivel, -nivel]
        t += 1
    return tempo, sinal

# Lista e mapeamento
codificacoes = [
    "NRZ-L", "NRZ-I", "AMI", "Pseudoternário",
    "Manchester", "Manchester Diferencial"
]

funcoes_codificacao = {
    "NRZ-L": nrzl,
    "NRZ-I": nrzi,
    "AMI": ami,
    "Pseudoternário": pseudoternario,
    "Manchester": manchester,
    "Manchester Diferencial": manchester_diferencial
}
