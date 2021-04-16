class ER:

    entrada = ""

    def __init__(self, entrada):
        self.entrada = entrada

    def getEntrada(self):
        return self.entrada

class AFN:

    def __init__(self, delta, estados_iniciais, estados_finais):
        self.delta = delta
        self.estados_iniciais = estados_iniciais
        self.estados_finais = estados_finais

    def getDelta(self):
        return self.delta

    def getEstadosIniciais(self):
        return self.estados_iniciais

    def getEstadosFinais(self):
        return self.estados_finais

class AFD:
    delta = {}
    estados_iniciais = []
    estados_finais = []

    def __init__(self, delta, estados_iniciais, estados_finais):
        self.delta = delta
        self.estados_iniciais = estados_iniciais
        self.estados_finais = estados_finais

    def getDelta(self):
        return self.delta

    def getEstadosIniciais(self):
        return self.estados_iniciais

    def getEstadosFinais(self):
        return self.estados_finais