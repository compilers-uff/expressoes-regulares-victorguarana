_idEstado = 0
Epslon = 'ε'
_SinaisInER = ['+', '*', '.']


def getIdEstado():
    global _idEstado
    _idEstado += 1
    return _idEstado


def afneToAFN(delta):
    afne = {}
    afne.update(delta)
    AFN = {}
    for estado in afne.keys():
        print(estado)
        transicao_limpa = []
        for transicao in afne[estado]:
            if ehTransicaoVazia(transicao):
                continue
            if getPalavra(transicao) == Epslon:
                transicao_limpa.extend(limparTransicaoEpslon(afne, transicao))
            else:
                transicao_limpa.extend(adicionarTransicoesComPalavra(afne, transicao))

        AFN[estado] = transicao_limpa

    return delta

def getPalavra(transicao):
    return transicao[0]

def getDestino(transicao):
    return transicao[1]

def ehTransicaoVazia(transicao):
    return len(transicao) == 0

def adicionarTransicoesComPalavra(afne, transicao_inicial):
    transicoes_limpas = []
    transicoes_limpas.append(transicao_inicial)
    palavra = getPalavra(transicao_inicial)
    estado_destino = getDestino(transicao_inicial)
    transicoes_limpas.extend(percorrerCaminhoEpsion(afne, palavra, estado_destino))

    return transicoes_limpas

def percorrerCaminhoEpsion(afne, palavra, estado_inicial):
    transicoes_limpas = []

    transacoes_atuais = afne[estado_inicial]
    for transicao_atual in transacoes_atuais:

        if (getPalavra(transicao_atual) != Epslon):
            continue

        else:
            estado_destino = getDestino(transicao_atual)

            transicoes_limpas.append([palavra, estado_destino])

            transicoes_limpas.extend(percorrerCaminhoEpsion(afne, palavra, estado_destino))

    return transicoes_limpas

def limparTransicaoEpslon(afne, transicao):
    transicoes_alternativas = encontrarCaminhosAlternativos(afne, transicao)

    transicoes_limpas = []

    for transicao_alternativa in transicoes_alternativas:
        palavra_alternativa = getPalavra(transicao_alternativa)
        transicoes_limpas.extend(percorrerCaminhoAlternativo(afne, palavra_alternativa, transicao_alternativa))

    return transicoes_limpas

def percorrerCaminhoAlternativo(afne, palavra, transicao_inicial):
    transicoes_limpas = []
    transicoes_limpas.append([palavra, getDestino(transicao_inicial)])

    #transacoes_atuais = afne[estado_inicial]
    #for transicao_atual in transacoes_atuais:
    estado_destino = getDestino(transicao_inicial)
    #transicoes_limpas.append([palavra, getDestino(transicao_inicial)])
    for transicao_destino in afne[estado_destino]:

        if (getPalavra(transicao_destino) == Epslon):

            estado_destino = getDestino(transicao_inicial)
            transicoes_limpas.extend(percorrerCaminhoAlternativo(afne, palavra, transicao_destino))

    return transicoes_limpas

def encontrarCaminhosAlternativos(afne, transicao):
    transicoes_base = []
    if getPalavra(transicao) != Epslon:
        transicoes_base.append(transicao)

    else:
        estado_destino = getDestino(transicao)
        for proxima_transicao in afne[estado_destino]:
            transicoes_base.extend(encontrarCaminhosAlternativos(afne, proxima_transicao))

    return transicoes_base


exemplo_afne1 = {'E7': [['ε', 'E8'], ['ε', 'E1']], 'E1': [['ε', 'E2'], ['ε', 'E4']], 'E2': ['mao', 'E3'], 'E3': ['ε', 'E6'], 'E4': ['pe', 'E5'], 'E5': ['ε', 'E6'], 'E6': [['ε', 'E1'], ['ε', 'E8']], 'E8': []}
exemplo_afne2 = {'E1': [['ε', 'E2'], ['ε', 'E4']], 'E2': [['a', 'E3']], 'E3': [['ε', 'E6']], 'E4': [['b', 'E5']], 'E5': [['ε', 'E6']], 'E6': [['ε', 'E7']], 'E7': [['c', 'E8']], 'E8': [['ε', 'E9']], 'E9': []}
transicoes_limpas = limparTransicaoEpslon(exemplo_afne2, ['ε', 'E2'])
delta = afneToAFN(exemplo_afne2)

##TODO evitar que percorrer caminho entre em loop