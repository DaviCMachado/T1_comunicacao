def decodificar_nrzl(sinal):    # FUNCIONA
    bits = []
    for nivel in sinal:
        if nivel == '-1':
            bits.append('1')  # -1 representa 1 no NRZ-L
        elif nivel == '1':
            bits.append('0')  # 1 representa 0 no NRZ-L
    return ''.join(bits)


def decodificar_nrzi(sinal):
    bits = []
    sinal = [x for x in sinal if x != '0']
    anterior = sinal[0]

    if anterior == '-1':
        atual = '0'
    elif anterior == '1':
        atual = '1'
    
    bits.append(atual)

    for nivel in sinal[1:]:
        if nivel == anterior:
            bits.append('0')
        else:
            bits.append('1')
        anterior = nivel
    return ''.join(bits)


def decodificar_ami(sinal):    # FUNCIONA
    bits = []
    for nivel in sinal:
        if nivel == '0':
            bits.append('0')  # 0 indica "0"
        elif nivel == '1' or nivel == '-1':
            bits.append('1')  # 1 ou -1 representam "1"
    return ''.join(bits)

def decodificar_pseudoternario(sinal):    # PARECE QUE FUNCIONA
    bits = []
    for nivel in sinal:
        if nivel == '0':
            bits.append('0')  # 0 indica "1"
        elif nivel == '1' or nivel == '-1':
            bits.append('1')  # 1 ou -1 indicam "0"
    return ''.join(bits)


def decodificar_manchester(sinal):         # TESTAR MAIS
    # 1) converte strings ['-1','1',...] em ints
    levels = [int(x) for x in sinal]
    bits = []
    
    # 2) percorre de 4 em 4
    for i in range(0, len(levels), 4):
        # compara o primeiro e o terceiro nível
        # se primeiro < terceiro → foi -1 → +1 (bit '1')
        if levels[i] < levels[i+2]:
            bits.append('1')
        else:
            bits.append('0')
    return ''.join(bits)


def decodificar_manchester_diferencial(sinal):     # TESTAR MAIS
    levels = [int(x) for x in sinal]
    bits = []
    # estado “anterior” = nível final do bit passado (última das 4 amostras)
    prev = levels[3]  # final do primeiro bit

    for i in range(4, len(levels), 4):
        # nível inicial do bit atual
        init = levels[i]
        # se init ≠ prev → houve inversão no início → bit '0'
        # se init == prev → sem inversão no início → bit '1'
        if init != prev:
            bits.append('0')
        else:
            bits.append('1')
        # atualiza prev para o final deste bit (levels[i+3])
        prev = levels[i+3]
    # incluir o primeiro bit:
    # sabemos que levels[0:4] já codificam o 1º bit
    # podemos decodificá-lo comparando levels[0] com o nível “de partida” (1)
    # mas como fixamos nivel inicial = 1, basta:
    first = '1' if levels[0] == 1 else '0'
    return first + ''.join(bits)


def decodificar_mlt3(sinal):             # TESTAR MAIS
    bits = []
    anterior = sinal[0]
    for nivel in sinal:
        if nivel != anterior:
            bits.append('1')
        else:
            bits.append('0')
        anterior = nivel
    return ''.join(bits)

# A 8B6T continua não implementada
def decodificar_8b6t(sinal):
    return "000"


# Lista e mapeamento
decodificacoes = [
    "NRZ-L", "NRZ-I", "AMI", "Pseudoternário",
    "Manchester", "Manchester Diferencial", "MLT-3", "8B/6T"
]

funcoes_decodificacao = {
    "NRZ-L": decodificar_nrzl,
    "NRZ-I": decodificar_nrzi,
    "AMI": decodificar_ami,
    "Pseudoternário": decodificar_pseudoternario,
    "Manchester": decodificar_manchester,
    "Manchester Diferencial": decodificar_manchester_diferencial,
    "MLT-3": decodificar_mlt3,
    "8B/6T": decodificar_8b6t
}
