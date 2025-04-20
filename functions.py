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

def b8zs(bits):
    tempo, sinal = [], []
    nivel = 1  # Polaridade inicial
    t = 0
    contadorZero = 0

    i = 0
    while i < len(bits):
        bit = bits[i]
        if bit == '1':
            contadorZero = 0
            tempo += [t, t + 0.5, t + 0.5, t + 1]
            nivel *=-1
            sinal += [0, 0, nivel, nivel]
        else:
            contadorZero += 1
            if contadorZero == 8:
                # Apaga os últimos 7 tempos e sinais de 0
                tempo = tempo[:-7*4]  # 7 bits * 4 tempos por bit
                sinal = sinal[:-7*4]

                # Para simplificar, vamos fazer a substituição manualmente
                seq = [0, 0, 0, nivel, -nivel, 0, -nivel, nivel]
                for bit_b8zs in seq:
                    tempo += [t, t + 0.5, t + 0.5, t + 1]
                    sinal += [0, 0, bit_b8zs, bit_b8zs]
                    t += 1
                contadorZero = 0
                i += 1
                continue
            else:
                tempo += [t, t + 0.5, t + 0.5, t + 1]
                sinal += [0, 0, 0, 0]
        t += 1
        i += 1

    return tempo, sinal


def four_b5b(bits):
    tabela = {
        '0000':'11110',
        '0001':'01001',
        '0010':'10100',
        '0011':'10101',
        '0100':'01010',
        '0101':'01011',
        '0110':'01110',
        '0111':'01111',
        '1000':'10010',
        '1001':'10011',
        '1010':'10110',
        '1011':'10111',
        '1100':'11010',
        '1101':'11011',
        '1110':'11100',
        '1111':'11101'
    }

    codificado=''
    quads = [bits[i:i+4] for i in range(0, len(bits), 4)]
    for quad in quads:
        if len(quad)<4:
            codificado = codificado+quad
        else:
            codificado = codificado+tabela[quad]

    # segundo wikpedia: ( https://en-m-wikipedia-org.translate.goog/wiki/4B5B?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc)
    # On optical fiber, the 4B5B output is NRZI-encoded. 
    # FDDI over copper (CDDI) uses MLT-3 encoding instead, as does 100BASE-TX Fast Ethernet.
    return nrzi(bits)
        


def mlt3(bits):
    pass

# Lista e mapeamento
codificacoes = [
    "NRZ-L", "NRZ-I", "AMI", "Pseudoternário",
    "Manchester", "Manchester Diferencial", "B8ZS",
    "4B5B","MLT-3"
]

funcoes_codificacao = {
    "NRZ-L": nrzl,
    "NRZ-I": nrzi,
    "AMI": ami,
    "Pseudoternário": pseudoternario,
    "Manchester": manchester,
    "Manchester Diferencial": manchester_diferencial,
    "B8ZS":b8zs,
    "4B5B":four_b5b,
    "MLT-3":mlt3
}
