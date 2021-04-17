from classes import AFN
Epslon = 'ε'

def afneToAFN(afne):

    delta_afne = afne.getDelta()
    delta_afn = limparEpsilon(delta_afne)

    estados_iniciais_afne = afne.getEstadosIniciais()
    estados_iniciais_afn = verificaSubEstados(delta_afn, estados_iniciais_afne)

    estados_finais_afne = afne.getEstadosFinais()
    estados_finais_afn = verificaSubEstados(delta_afn, estados_finais_afne)

    afn = AFN(delta_afn, estados_iniciais_afn, estados_finais_afn)

    return afn


def limparEpsilon(afne):
    #print("AFNe :")
    #print(afne)
    AFN = {}
    for estado in afne.keys():
        transicao_limpa = []
        for transicao in afne[estado]:
            if ehTransicaoVazia(transicao):
                continue
            if getPalavra(transicao) == Epslon:
                transicao_limpa.extend(limparTransicaoEpslon(afne, estado, transicao))
            else:
                transicao_limpa.extend(adicionarTransicoesComPalavra(afne, estado, transicao))

        AFN[estado] = transicao_limpa
    #print("AFN:")
    #print(AFN)
    return AFN

def getPalavra(transicao):
    return transicao[0]

def getDestino(transicao):
    return transicao[1]

def ehTransicaoVazia(transicao):
    return len(transicao) == 0

def adicionarTransicoesComPalavra(afne, estado_inicial, transicao_inicial):
    transicoes_limpas = []

    # lista para evitar repetição/loop infinito
    estados_visitados = [estado_inicial]

    #adiciona transicao inicial
    transicoes_limpas.append(transicao_inicial)

    #Procura outras transicoes possiveis a partir do estado destino
    palavra = getPalavra(transicao_inicial)
    estado_destino = getDestino(transicao_inicial)
    transicoes_limpas.extend(percorrerCaminhoEpsion(afne, palavra, estado_destino, estados_visitados))

    return transicoes_limpas

#Procura outras transicoes possiveis a partir do estado destino
def percorrerCaminhoEpsion(afne, palavra, estado_inicial, estados_visitados):
    transicoes_limpas = []

    # adiciona estado atual p/ evitar repetição/loop infinito
    estados_visitados.append(estado_inicial)

    transacoes_atuais = afne[estado_inicial]
    for transicao_atual in transacoes_atuais:

        if getPalavra(transicao_atual) != Epslon:
            continue

        else:
            estado_destino = getDestino(transicao_atual)

            # verifica se proximo estado já foi visitado
            if estado_destino in estados_visitados:
                continue

            transicoes_limpas.append((palavra, estado_destino))

            transicoes_limpas.extend(percorrerCaminhoEpsion(afne, palavra, estado_destino, estados_visitados))

    return transicoes_limpas

def limparTransicaoEpslon(afne, estado_inicial, transicao):
    #Lista para evitar recursão infinita
    estados_visitados = [estado_inicial]

    #Encontrando todos os caminhos possiveis para essa transição
    transicoes_alternativas = encontrarCaminhosAlternativos(afne, transicao, estados_visitados)

    transicoes_limpas = []

    #Percorrenso os caminhos possiveis
    for transicao_alternativa in transicoes_alternativas:
        palavra_alternativa = getPalavra(transicao_alternativa)
        transicoes_limpas.extend(percorrerCaminhoAlternativo(afne, palavra_alternativa, transicao_alternativa, estados_visitados))

    return transicoes_limpas

def encontrarCaminhosAlternativos(afne, transicao, estados_visitados):
    transicoes_base = []
    if getPalavra(transicao) != Epslon:
        transicoes_base.append(transicao)

    else:
        #Evitando recursões infinitas
        estado_destino = getDestino(transicao)
        if estado_destino in estados_visitados:
            return transicoes_base
        estados_visitados.append(estado_destino)
        #Continua buscando novos caminhos
        for proxima_transicao in afne[estado_destino]:
            transicoes_base.extend(encontrarCaminhosAlternativos(afne, proxima_transicao, estados_visitados))

    return transicoes_base

def percorrerCaminhoAlternativo(afne, palavra, transicao_inicial, estados_visitados):
    transicoes_limpas = []
    transicoes_limpas.append((palavra, getDestino(transicao_inicial)))

    #evitando recursão infinita
    estado_destino = getDestino(transicao_inicial)
    if estado_destino in estados_visitados:
        return transicoes_limpas
    estados_visitados.append(estado_destino)

    for transicao_destino in afne[estado_destino]:

        if (getPalavra(transicao_destino) == Epslon):

            transicoes_limpas.extend(percorrerCaminhoAlternativo(afne, palavra, transicao_destino, estados_visitados))

    return transicoes_limpas

def verificaSubEstados(delta, estados):
    for estado in delta.keys():
        if estado in estados:
            continue

        sub_estados = estado.split(',')
        pertence = any(estado in sub_estados for estado in estados)
        if pertence:
            estados += estado

    return estados

#delta = {'E1': [('ε', 'E2'), ('ε', 'E4')], 'E2': [('a', 'E3')], 'E3': [('ε', 'E6')], 'E4': [('b', 'E5')], 'E5': [('ε', 'E6')], 'E6': [('ε', 'E7')], 'E7': [('c', 'E8')], 'E8': [('ε', 'E9')], 'E9': []}
#estados_iniciais = ['E1']
#estados_finais = ['E9']
#exemplo_afne = AFN(delta, estados_iniciais, estados_finais)
#afneToAFN(exemplo_afne)