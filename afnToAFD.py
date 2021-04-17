from classes import AFN
from classes import AFD

Epslon = 'ε'

_EstadosConcluidos = [] # Ex: ['E1', 'E2', 'E1,E2']

def addEstadoConcluido(estado):
    _EstadosConcluidos.append(estado)

def ehEstadoConcluido(estado):
    return estado in _EstadosConcluidos


def afnToAFD(afn):

    delta_afd = {}
    delta = afn.getDelta()

    #valida as transicoes (Remove transicoes de uma palavra para multiplos destinos)
    for estado in delta.keys():

        delta_afd_aux = validarTransicoes(delta, estado)
        delta_afd.update(delta_afd_aux)

    #Verificar determinismo
    delta_afd = verificaDeterminismo(delta_afd)


    estados_iniciais_afn = afn.getEstadosIniciais()
    estados_iniciais_afd = verificaSubEstados(delta_afd, estados_iniciais_afn)

    estados_finais_afn = afn.getEstadosFinais()
    estados_finais_afd = verificaSubEstados(delta_afd, estados_finais_afn)


    afd = AFD(delta_afd, estados_iniciais_afd, estados_finais_afd)

    return afd

def getPalavra(transicao):
    return transicao[0]

def getDestino(transicao):
    return transicao[1]

# Verifica transforma multiplas transicoes em uma transicao com um grupo de estados
def validarTransicoes(delta, estados):

    estados_destinos = {}   # { palavra : [estados] }
    transicoes = []
    delta_aux = {}   # { estado : [palavra, destino]] }

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
        transicoes.extend(delta[estado])

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
    delta_aux[novo_estado] = []
    for palavra in estados_destinos.keys():
        estado_destino = ','.join(estados_destinos[palavra])
        delta_aux[novo_estado] += [(palavra, estado_destino)]

    for palavra in estados_destinos.keys():
        delta_aux.update(validarTransicoes(delta, estados_destinos[palavra]))

    return delta_aux

def pegaPalavrasAFD(afd):
    palavras = []
    for estado in afd.keys():
        for transicao in afd[estado]:
            palavra = getPalavra(transicao)
            if not palavra in palavras:
                palavras.append(palavra)

    return palavras

def verificaDeterminismo(delta):
    palavras = pegaPalavrasAFD(delta)
    estados = delta.keys()

    #determina estado buraco
    estado_id = 0
    estado_buraco = 'E' + str(estado_id)
    while estado_buraco in estados:
        estado_id += 1
        estado_buraco = 'E' + str(estado_id)

    buraco_usado = False
    for estado in estados:

        #verifica qual palavra esta faltando
        palavras_faltando = palavras.copy()
        for transicao in delta[estado]:
            palavra_atual = getPalavra(transicao)
            if palavra_atual in palavras_faltando:
                palavras_faltando.remove(palavra_atual)


        for palavra in palavras_faltando:
            delta[estado].append((palavra, estado_buraco))
            buraco_usado = True

    if buraco_usado:
        delta[estado_buraco] = []
        for palavra in palavras:
            delta[estado_buraco].append((palavra, estado_buraco))


    return delta

def verificaSubEstados(delta, estados):
    for estado in delta.keys():
        if estado in estados:
            continue

        sub_estados = estado.split(',')
        pertence = any(estado in sub_estados for estado in estados)
        if pertence:
            estados.append(estado)

    return estados

#delta = {'E1': [('a', 'E3'), ('a', 'E6'), ('a', 'E7'), ('b', 'E5'), ('b', 'E6'), ('b', 'E7')], 'E2': [('a', 'E3'), ('a', 'E6'), ('a', 'E7')], 'E3': [('c', 'E8'), ('c', 'E9')], 'E4': [('b', 'E5'), ('b', 'E6'), ('b', 'E7')], 'E5': [('c', 'E8'), ('c', 'E9')], 'E6': [('c', 'E8'), ('c', 'E9')], 'E7': [('c', 'E8'), ('c', 'E9')], 'E8': [], 'E9': []}
#estados_iniciais = ['E1']
#estados_finais = ['E9']
#exemplo_afn = AFN(delta, estados_iniciais, estados_finais)
#afnToAFD(exemplo_afn)
