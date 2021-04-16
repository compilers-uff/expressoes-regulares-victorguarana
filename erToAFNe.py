from classes import ER
from classes import AFN

Epslon = 'ε'
_SinaisInER = ['+', '*', '.']

_idEstado = 0
def getIdEstado():
    global _idEstado
    _idEstado += 1
    return _idEstado

def erToAFNe(er):
    entrada = er.getEntrada()

    # pega o delta organizado linearmente
    delta = criarDelta(entrada)

    estados = list(delta.keys())
    estado_inicial = estados[0]
    estado_final = estados[-1]
    afne = AFN(delta, [estado_inicial], [estado_final])

    return afne

def criarDelta(er):
    delta = {}
    if temSinal(er):
        sinal = getSinal(er)

        esquerda_geral = getEsquerda(er)
        direita_geral = getDireita(er, esquerda_geral)

        # Parada da recursão
        if not temSinal(esquerda_geral) and not temSinal(direita_geral):
            delta = adicionaDeltaInicial(sinal, esquerda_geral, direita_geral, delta)

            # return delta

        # Recursão caso tenha mais algum sinal
        # Ambos os lados tem sinais -> Recursão em ambos
        if temSinal(esquerda_geral) and temSinal(direita_geral):

            delta_esquerda = criarDelta(esquerda_geral)
            delta_direita = criarDelta(direita_geral)

            delta = operacaoDeltaDuplo(sinal, delta, delta_esquerda, delta_direita)

            # return delta

        # Somente a esquerda tem sinal
        elif (temSinal(esquerda_geral)):

            # entra na recursão
            delta_esquerda = criarDelta(esquerda_geral)

            # Pega palavra da direita
            if (not temSinal(direita_geral)):
                delta = operacaoDeltaEsquerda(sinal, delta_esquerda, direita_geral)

        # Somente a direita tem sinal
        elif (temSinal(direita_geral)):
            # entra na recursão
            delta_direita = criarDelta(direita_geral)

            # Pega palavra da direita
            if (not temSinal(esquerda_geral)):
                delta = operacaoDeltaEsquerda(sinal, delta_direita, esquerda_geral)

        # Cotinuação do sinal atual

    else:
        delta = adicionaDeltaUnico(er)

    print("============================================================")
    print("ER: " + er)
    print(delta)
    print("============================================================")
    print("\n")
    return delta


def temSinal(er):
    if er != '':
        return er[0] in _SinaisInER

    return False

def getSinal(er):
    return er[0]

def getEsquerda(er):
    er_esquerda = ""

    # com operação
    if er[2] in _SinaisInER:

        # auxiliares
        qnt_parenteses_abertos = 0
        comecou = False

        # removendo primeira operação e primeiro parenteses
        er = er[2:]
        for x in er:
            er_esquerda += x
            if x == "(":
                qnt_parenteses_abertos += 1
                comecou = True
            elif x == ")":
                qnt_parenteses_abertos -= 1

            if comecou and qnt_parenteses_abertos == 0:
                break

    # Sem operação
    else:
        virgula_index = er.rindex(',')
        er_esquerda = er[2:virgula_index]

    # print(er_esquerda)
    return er_esquerda

def getDireita(er, esquerda):
    if getSinal(er) == '*':
        return ""
    er_direita = ""
    pos_inicial_esq = er.index(esquerda)
    pos_final_esq = pos_inicial_esq + len(esquerda)
    er = er[pos_final_esq:]
    # com operação
    if er[2] in _SinaisInER:

        # auxiliares
        qnt_parenteses_abertos = 0
        comecou = False

        # removendo primeira operação e primeiro parenteses
        er = er[2:]
        for x in er:
            er_direita += x
            if x == "(":
                qnt_parenteses_abertos += 1
                comecou = True
            elif x == ")":
                qnt_parenteses_abertos -= 1

            if comecou and qnt_parenteses_abertos == 0:
                break

    # Sem operação
    else:
        virgula_index = er.index(')')
        er_direita = er[2:virgula_index]

    # print(er_direita)
    return er_direita

def getEstadoInicial(delta):
    chave = list(delta.keys())[0]
    return chave

def getEstadoFinal(delta):
    chave = list(delta.keys())[-1]
    return chave

def adicionaDeltaUnico(palavra):
    delta = {}
    estado1 = "E" + str(getIdEstado())
    estado2 = "E" + str(getIdEstado())

    delta[estado1] = [(palavra, estado2)]
    delta[estado2] = []

    return delta

def adicionaDeltaInicial(sinal, inicio, final, delta):
    if sinal == '+':
        #print("Operação: " + inicio + sinal + final)
        estado1 = "E" + str(getIdEstado())
        estado2 = "E" + str(getIdEstado())
        estado3 = "E" + str(getIdEstado())
        estado4 = "E" + str(getIdEstado())
        estado5 = "E" + str(getIdEstado())
        estado6 = "E" + str(getIdEstado())
        # Conectando AFNe's

        delta[estado1] = [(Epslon, estado2), (Epslon, estado4)]
        delta[estado2] = [(inicio, estado3)]
        delta[estado3] = [(Epslon, estado6)]
        delta[estado4] = [(final, estado5)]
        delta[estado5] = [(Epslon, estado6)]
        delta[estado6] = []

    elif sinal == '*':
        #print("Operação: " + inicio + sinal)
        estado1 = "E" + str(getIdEstado())
        estado2 = "E" + str(getIdEstado())
        estado3 = "E" + str(getIdEstado())
        estado4 = "E" + str(getIdEstado())

        delta[estado1] = [(Epslon, estado2), (Epslon, estado4)]
        delta[estado2] = [(inicio, estado3)]
        delta[estado3] = [(Epslon, estado2), (Epslon, estado4)]
        delta[estado4] = []

    elif sinal == '.':
        #print("Operação: " + inicio + final)
        estado1 = "E" + str(getIdEstado())
        estado2 = "E" + str(getIdEstado())
        estado3 = "E" + str(getIdEstado())
        estado4 = "E" + str(getIdEstado())

        delta[estado1] = [(inicio, estado2)]
        delta[estado2] = [(Epslon, estado3)]
        delta[estado3] = [(final, estado4)]
        delta[estado4] = []

    # print("Resultado: ")
    # print(delta)
    return delta

def operacaoDeltaEsquerda(sinal, delta_esquerda, direita):
    delta = {}
    if sinal == '+':
        estado_inicial_esquerda = getEstadoInicial(delta_esquerda)
        estado_final_esquerda = getEstadoFinal(delta_esquerda)
        estado_direita1 = "E" + str(getIdEstado())
        estado_direita2 = "E" + str(getIdEstado())
        estado_inicial_geral = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_inicial_esquerda), (Epslon, estado_direita1)]

        delta.update(delta_esquerda)

        delta[estado_direita1] = [(direita, estado_direita2)]
        delta[estado_direita2] = [(Epslon, estado_final_geral)]

        delta[estado_final_esquerda] = [(Epslon, estado_final_geral)]

        delta[estado_final_geral] = []

    elif sinal == '*':
        estado_inicial_esquerda = getEstadoInicial(delta_esquerda)
        estado_final_esquerda = getEstadoFinal(delta_esquerda)
        estado_inicial_geral = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_final_geral), (Epslon, estado_inicial_esquerda)]
        delta.update(delta_esquerda)
        delta[estado_final_esquerda] = [(Epslon, estado_inicial_esquerda), (Epslon, estado_final_geral)]
        delta[estado_final_geral] = []

    elif sinal == '.':
        estado_final_esquerda = getEstadoFinal(delta_esquerda)
        estado_direita1 = "E" + str(getIdEstado())
        estado_direita2 = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta.update(delta_esquerda)

        delta[estado_final_esquerda] = [(Epslon, estado_direita1)]
        delta[estado_direita1] = [(direita, estado_direita2)]
        delta[estado_direita2] = [(Epslon, estado_final_geral)]

        delta[estado_final_geral] = []

    # print(delta)
    return delta

def operacaoDeltaDireita(sinal, esquerda, delta_direita):
    delta = {}
    if sinal == '+':
        estado_inicial_direita = getEstadoInicial(delta_direita)
        estado_final_direita = getEstadoFinal(delta_direita)
        estado_esquerda1 = "E" + str(getIdEstado())
        estado_esquerda2 = "E" + str(getIdEstado())
        estado_inicial_geral = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_inicial_direita), (Epslon, estado_esquerda1)]

        delta[estado_esquerda1] = [(esquerda, estado_esquerda2)]
        delta[estado_esquerda2] = [(Epslon, estado_final_geral)]

        delta.update(delta_direita)

        delta[estado_final_direita] = [(Epslon, estado_final_geral)]

        delta[estado_final_geral] = []

    elif sinal == '*':
        estado_inicial_direita = getEstadoInicial(delta_direita)
        estado_final_direita = getEstadoFinal(delta_direita)
        estado_inicial_geral = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_final_geral), (Epslon, estado_inicial_direita)]
        delta.update(delta_direita)
        delta[estado_final_direita] = [(Epslon, estado_inicial_direita), (Epslon, estado_final_geral)]

    elif sinal == '.':
        estado_inicial_direita = getEstadoInicial(delta_direita)
        estado_esquerda1 = "E" + str(getIdEstado())
        estado_esquerda2 = "E" + str(getIdEstado())
        estado_inicial_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_esquerda1)]
        delta[estado_esquerda1] = [(esquerda, estado_esquerda2)]
        delta[estado_esquerda2] = [(Epslon, estado_inicial_direita)]

        delta.update(delta_direita)

    # print(delta)
    return delta

def operacaoDeltaDuplo(sinal, delta, delta_esquerda, delta_direita):
    if sinal == '+':
        estado_inicial_esquerda = getEstadoInicial(delta_esquerda)
        estado_final_esquerda = getEstadoFinal(delta_esquerda)
        estado_inicial_direita = getEstadoInicial(delta_direita)
        estado_final_direita = getEstadoFinal(delta_direita)
        estado_inicial_geral = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_inicial_esquerda), (Epslon, estado_inicial_direita)]

        delta.update(delta_esquerda)
        delta[estado_final_esquerda] = [(Epslon, estado_final_geral)]
        delta.update(delta_direita)
        delta[estado_final_direita] = [(Epslon, estado_final_geral)]

        delta[estado_final_geral] = []

    elif sinal == '*':
        estado_inicial_esquerda = getEstadoInicial(delta_esquerda)
        estado_final_esquerda = getEstadoFinal(delta_esquerda)
        estado_inicial_geral = "E" + str(getIdEstado())
        estado_final_geral = "E" + str(getIdEstado())

        delta[estado_inicial_geral] = [(Epslon, estado_final_geral), (Epslon, estado_inicial_esquerda)]
        delta[estado_final_esquerda] = [(Epslon, estado_inicial_esquerda), (Epslon, estado_final_geral)]
        delta[estado_final_geral] = []

    elif sinal == '.':
        estado_final_esquerda = getEstadoFinal(delta_esquerda)
        estado_inicial_direita = getEstadoInicial(delta_direita)
        estado_final_geral = "E" + str(getIdEstado())

        delta.update(delta_esquerda)
        delta.update(delta_direita)

        delta[estado_final_esquerda] = [(Epslon, estado_inicial_direita), (Epslon, estado_final_geral)]

        delta[estado_final_geral] = []

    # print(delta)
    return delta

exemplo_er1 = ER(".(+(a, b), c)")
erToAFNe(exemplo_er1)