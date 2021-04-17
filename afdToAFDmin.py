from classes import AFD

_pares_nao_verificados = []
_pares_equivalentes = []
_pares_nao_equivalentes = []

def addParNaoVerfificados(par):
    par = tuple(sorted((par)))
    _pares_nao_verificados.append(par)

def addParNaoEquivalente(par):
    par = tuple(sorted((par)))
    _pares_nao_equivalentes.append(par)
    _pares_nao_verificados.remove(par)

def addParEquivalente(par):
    par = tuple(sorted((par)))
    _pares_equivalentes.append(par)
    _pares_nao_verificados.remove(par)

def ehParEquivalente(par):
    par = tuple(sorted((par)))
    if par in _pares_equivalentes or par[0] == par[1]:
        return True
    return False

def getListaDeParesNaoVerificados():
    return _pares_nao_verificados.copy()

def getListaDeParesEquivalentes():
    return _pares_equivalentes.copy()

def getPrimeiroPar():
    return

def afdToAFDmin(afd):
    delta_afd = afd.getDelta()

    estados_iniciais = afd.getEstadosIniciais()
    estados_finais = afd.getEstadosFinais()

    delta_afd = eliminaEstadosInuteis(delta_afd, estados_iniciais)


    verificarEquivalencias(delta_afd, estados_iniciais, estados_finais)

    delta_afd = eliminarEstadosEquivalentes(delta_afd)

    estados_iniciais = afd.getEstadosIniciais()
    estados_finais = afd.getEstadosFinais()

    afd_min = AFD(delta_afd, estados_iniciais, estados_finais)

    return afd_min


def getPalavra(transicao):
    return transicao[0]


def getDestino(transicao):
    return transicao[1]


def eliminaEstadosInuteis(delta, estados_iniciais):
    delta_aux = delta.copy()
    # Verifica se estado é alcancavel por algum outro

    alteracaoFeita = False
    for estado_verificacao in delta.keys():

        if estado_verificacao in estados_iniciais:
            continue

        ehUtil = False

        for estado_origem in delta.keys():
            if estado_origem == estado_verificacao:
                continue

            if ehUtil:
                break

            transicoes = delta[estado_origem]
            for transicao in transicoes:
                if getDestino(transicao) == estado_verificacao:
                    ehUtil = True
                    break

        if not ehUtil:
            delta_aux.pop(estado_verificacao)
            alteracaoFeita = True

    if alteracaoFeita:
        delta_aux = eliminaEstadosInuteis(delta_aux, estados_iniciais)

    return delta_aux


def pegarTodosEstados(delta):
    estados = list(delta.keys())
    return estados


def naoEquivalenteTrivial(par_estados, estados_finais):
    if (par_estados[0] in estados_finais and par_estados[1] not in estados_finais):
        return True
    if (par_estados[0] not in estados_finais and par_estados[1] in estados_finais):
        return True
    return False


def verificarEquivalencias(delta, estados_iniciais, estados_finais):

    #Salvar todos os pares de estados
    estados = list(delta.keys())
    pares = []
    estados = sorted(estados)
    tamanho = len(estados)
    for i in range(tamanho):
        for j in range(i+1, tamanho):
            addParNaoVerfificados((estados[i], estados[j]))


    pares_nao_verificados = getListaDeParesNaoVerificados()

    # Equivalencias triviais
    for par_estado in pares_nao_verificados:
        if naoEquivalenteTrivial(par_estado, estados_finais):
            addParNaoEquivalente(par_estado)

    # Equivalencia não trivial
    alteracao = True
    while alteracao:
        alteracao = False
        pares_nao_verificados = getListaDeParesNaoVerificados()
        for par in pares_nao_verificados:
            if ehEquivalenciaNaoTrivial(delta, par):
                addParEquivalente(par)
                alteracao = True


def ehEquivalenciaNaoTrivial(delta, par):

    pares_destinos = []

    for i in range(len(delta[par[0]])-1):
        transicao1 = delta[par[0]][i]
        transicao2 = delta[par[1]][i]
        destino1 = getDestino(transicao1)
        destino2 = getDestino(transicao2)
        par = tuple(sorted([destino1, destino2]))
        pares_destinos.append(par)


    #retorna false se não tiver nenhum equivalente
    for par_destino in pares_destinos:
        if not ehParEquivalente(par_destino):
            return False

    # retorna true caso todos sejam equivalentes
    return True

def eliminarEstadosEquivalentes(delta):

    #verificar se existe um elemento em mais de um par

    #dicionario de substituição
    pares_equivalentes = getListaDeParesEquivalentes()
    substituicao = {}
    total_pares = (len(pares_equivalentes))
    total_elementos = total_pares * 2

    elemento_atual = 0
    par_atual = 0

    for j in range(total_elementos):
        elemento_pivo = pares_equivalentes[par_atual][elemento_atual]
        if elemento_pivo not in substituicao.keys():
            substituicao[elemento_pivo] = elemento_pivo
            if elemento_atual == 0:
                prox_equivalente = pares_equivalentes[par_atual][elemento_atual + 1]
                substituicao[prox_equivalente] = elemento_pivo

        par_index = 0
        elemento_index = 0

        for i in range(total_elementos):
            if (i == j):
                elemento_index += 1
                if elemento_index / 2 >= 1:
                    elemento_index = 0
                    par_index += 1
                continue

            elemento_comparacao = pares_equivalentes[par_index][elemento_index]

            if (elemento_pivo == elemento_comparacao):
                index_aux = 0
                if elemento_index == 0:
                    index_aux = 1
                elemento_equivalente = pares_equivalentes[par_index][index_aux]
                if elemento_equivalente not in substituicao.keys():
                    substituicao[elemento_equivalente] = substituicao[elemento_pivo]

            elemento_index += 1
            if elemento_index / 2 >= 1:
                elemento_index = 0
                par_index += 1

        elemento_atual += 1
        if elemento_atual / 2 >= 1:
            elemento_atual = 0
            par_atual += 1

    estados_excluidos = []
    delta_aux = {}
    for estado_atual in delta.keys():

        if estado_atual in substituicao.keys():
            if estado_atual != substituicao[estado_atual]:
                estados_excluidos.append(estado_atual)
                continue

        delta_aux[estado_atual] = delta[estado_atual]

    for estado_atual in delta_aux.keys():
        for i in range(len(delta_aux[estado_atual])-1):
            transicao = delta_aux[estado_atual][i]
            destino = getDestino(transicao)
            if destino in estados_excluidos:
                palavra = getPalavra(transicao)
                transicao = (palavra, substituicao[destino])
                delta_aux[estado_atual][i] = transicao

    return delta_aux

#delta = {'E1': [('a', 'E3,E6,E7'), ('b', 'E5,E6,E7'), ('c', 'E0')], 'E3,E6,E7': [('c', 'E8,E9'), ('a', 'E0'), ('b', 'E0')], 'E8,E9': [('a', 'E0'), ('b', 'E0'), ('c', 'E0')], 'E5,E6,E7': [('c', 'E8,E9'), ('a', 'E0'), ('b', 'E0')], 'E2': [('a', 'E3,E6,E7'), ('b', 'E0'), ('c', 'E0')], 'E3': [('c', 'E8,E9'), ('a', 'E0'), ('b', 'E0')], 'E4': [('b', 'E5,E6,E7'), ('a', 'E0'), ('c', 'E0')], 'E5': [('c', 'E8,E9'), ('a', 'E0'), ('b', 'E0')], 'E6': [('c', 'E8,E9'), ('a', 'E0'), ('b', 'E0')], 'E7': [('c', 'E8,E9'), ('a', 'E0'), ('b', 'E0')], 'E8': [('a', 'E0'), ('b', 'E0'), ('c', 'E0')], 'E9': [('a', 'E0'), ('b', 'E0'), ('c', 'E0')]}
#estados_iniciais = ['E1']
#estados_finais = ['E1']
#exemplo_afd1 = AFD(delta, estados_iniciais, estados_finais)
#afdToAFDmin(exemplo_afd1)
