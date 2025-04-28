# --- Codificações implementadas ---

import tabelas

def nrzl(bits):
    tempo, sinal = [], []
    t = 0
    for bit in bits:
        tempo += [t, t + 1]
        sinal += [1 if bit == '0' else -1] * 2 
        t += 1
    return tempo, sinal


def nrzi(bits):
    tempo, sinal = [], []
    
    if not bits:
        return tempo, sinal

    nivel = -1 if bits[0] == '0' else 1

    t = 0
    for i, bit in enumerate(bits):
        if i > 0 and bit == '1':
            nivel *= -1  # Inverte nível no bit '1', exceto no primeiro bit
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
    nivel = 1  # Pode começar em 1 ou -1, é arbitrário
    t = 0
    for bit in bits:
        if bit == '0':
            nivel *= -1  # transição no início
        tempo += [t, t + 0.5, t + 0.5, t + 1]
        sinal += [nivel, nivel, -nivel, -nivel]  # transição no meio
        nivel = -nivel  # prepara para o próximo bit (fim = início do próximo)
        t += 1
    return tempo, sinal


def mlt3(bits):
    nivel = 0
    t = 1
    tempo, sinal = [], []
    ultimoNivelNaoNulo = 1 #primeiro '1' faz tensão ir p baixo
    for bit in bits:
        if bit == '1':
            if len(sinal)==0 or sinal[-1] == 0:
                ultimoNivelNaoNulo *=-1
                nivel = ultimoNivelNaoNulo
            elif sinal[-1] == 1 or sinal[-1] == -1:
                nivel = 0 

        elif bit == '0': #faz nada, mantém valores.
            pass

        tempo += [t, t+1]
        sinal += [nivel]*2

        t += 1
        
    return tempo, sinal


def _8b6t(bits):
    mapeamento = tabelas.mapeamento8b6t()

    if (len(bits) %8) != 0: #necessário ser sequencia de BYTES!!!!
        return [], []

    sinal = []
    tempo = []
    
    # Processa cada byte (8 bits) da sequência
    t = 0
    for i in range(0, len(bits), 8):
        bitStr = bits[i:i+8] #"00000110"
        chave = int(bitStr, 2) # 0b0 == 0 == 0x0
        if chave not in mapeamento:
            raise ValueError(f"Byte inválido: {chave}")
        
        sinais = mapeamento[chave]
        
        sinal+=sinais
        
        tempo += [t, t+1, t+2, t+3, t+4, t+5]
        t+=6
    return tempo, sinal

def four_dpam5(bits): #four dimensional, five-level pulse amplitude modulation !!confirmar tensão dos valores
    """Codifica bits em sinais PAM5 com tempo e sinal, estilo NRZL."""
    tempo, sinal = [], []
    if len(bits) %8!=0:
        return tempo, sinal
    
    mapaSinais= tabelas.mapeamento4dpam5()
    
    t=0
    for bit1, bit2 in zip(bits[::2], bits[1::2]):
        tempo+=[t, t+1]
        sinal+=[mapaSinais[bit1+bit2]]*2
        t+=1

    return tempo, sinal

# Lista e mapeamento
codificacoes = [
    "NRZ-L", "NRZ-I", "AMI", "Pseudoternário",
    "Manchester", "Manchester Diferencial",
    "MLT-3", "8B/6T", "4D-PAM5"
]

funcoes_codificacao = {
    "NRZ-L": nrzl,
    "NRZ-I": nrzi,
    "AMI": ami,
    "Pseudoternário": pseudoternario,
    "Manchester": manchester,
    "Manchester Diferencial": manchester_diferencial,
    "MLT-3":mlt3,
    "8B/6T":_8b6t,
    "4D-PAM5":four_dpam5
}