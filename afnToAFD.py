Epslon = 'ε'

_EstadosConcluidos = [] # Ex: ['E1', 'E2', 'E1,E2']

def addEstadoConcluido(estado):
    _EstadosConcluidos.append(estado)

def ehEstadoConcluido(estado):
    return estado in _EstadosConcluidos


def afnToAFD(afn):
    print("AFN:")
    print(afn)
    AFD = {}

    #valida as transicoes (Remove transicoes de uma palavra para multiplos destinos)
    for estado in afn.keys():

        AFD_aux = validarTransicoes(afn, estado)
        AFD.update(AFD_aux)

    #Verificar determinismo
    verificaDeterminismo(AFD)


    print("AFD:")
    print(AFD)
    return AFD

def getPalavra(transicao):
    return transicao[0]

def getDestino(transicao):
    return transicao[1]

# Verifica transforma multiplas transicoes em uma transicao com um grupo de estados
def validarTransicoes(afn, estados):

    estados_destinos = {}   # { palavra : [estados] }
    transicoes = []
    afd_auxiliar = {}   # { estado : [palavra, destino]] }

    if type(estados) == list:
    # cria nomenclatura do novo estado
        estados = sorted(estados)
        novo_estado = ','.join(estados)

    else:
        novo_estado = estados
        estados = [estados]

    #Sai caso o estado já tenha sido concluido
    if ehEstadoConcluido(novo_estado):
        return {}
    else:
        addEstadoConcluido(novo_estado)

    #pega todas as transicoes possiveis
    for estado in estados:
        transicoes.extend(afn[estado])

    # Verifica estados destinos por palavra
    for transicao in transicoes:
        palavra = getPalavra(transicao)

        # Adiciona destino ao dicionario de estados destinos
        if palavra in estados_destinos.keys():
            if not getDestino(transicao) in estados_destinos[palavra]:
                estados_destinos[palavra] += [getDestino(transicao)]

        # Adiciona palavra nova ao dicionario de possibilidades
        else:
            estados_destinos[palavra] = [getDestino(transicao)]

    #cria afd com dados obtidos
    afd_auxiliar[novo_estado] = []
    for palavra in estados_destinos.keys():
        estado_destino = ','.join(estados_destinos[palavra])
        afd_auxiliar[novo_estado] += [[palavra, estado_destino]]

    for palavra in estados_destinos.keys():
        afd_auxiliar.update(validarTransicoes(afn, estados_destinos[palavra]))

    return afd_auxiliar

def pegaPalavrasAFD(afd):
    palavras = []
    for estado in afd.keys():
        for transicao in afd[estado]:
            palavra = getPalavra(transicao)
            if not palavra in palavras:
                palavras.append(palavra)

    return palavras

def verificaDeterminismo(afd):
    palavras = pegaPalavrasAFD(afd)
    estados = afd.keys()

    #determina estado buraco
    estado_id = 0
    estado_buraco = 'E' + str(estado_id)
    while estado_buraco in estados:
        estado_id += 1
        estado_buraco = 'E' + str(estado_id)


    for estado in estados:

        #verifica qual palavra esta faltando
        palavras_faltando = palavras.copy()
        for transicao in afd[estado]:
            palavra_atual = getPalavra(transicao)
            if palavra_atual in palavras_faltando:
                palavras_faltando.remove(palavra_atual)


        for palavra in palavras_faltando:
            afd[estado].append([palavra, estado_buraco])

    return afd

exemplo_afne1 = {'E1': [['a', 'E3'], ['a', 'E6'], ['a', 'E7'], ['b', 'E5'], ['b', 'E6'], ['b', 'E7']], 'E2': [['a', 'E3'], ['a', 'E6'], ['a', 'E7']], 'E3': [['c', 'E8'], ['c', 'E9']], 'E4': [['b', 'E5'], ['b', 'E6'], ['b', 'E7']], 'E5': [['c', 'E8'], ['c', 'E9']], 'E6': [['c', 'E8'], ['c', 'E9']], 'E7': [['c', 'E8'], ['c', 'E9']], 'E8': [], 'E9': []}
delta = afnToAFD(exemplo_afne1)
