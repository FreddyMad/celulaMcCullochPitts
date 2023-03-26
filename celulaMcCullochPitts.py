from numpy import random

class McCullochPittss():
    
    def __init__(self, compuerta = "AND", epoch = 100, n_bits = 2):
        self.n_bits = n_bits
        self.cumpuerta = compuerta
        self.epoch = epoch
        if compuerta == "NOT":
            print("Para la compuerta NOT el numero de bits por defecto es 1")
            self.n_bits = 1
        self.tdv = self.tabla_de_verdad(self.n_bits, self.cumpuerta)
        self.pesos_sinapticos = []
        self.umbral = None

    def tabla_de_verdad(self, n_bits, compuerta = "AND"):
        matriz = []
        aux = {}
        tdv = {}
        for i in range(n_bits):
            aux[i] = 2**(n_bits-(i+1))
        for k, j in aux.items():
            matriz.insert(k,[])
            bit_actual = 1
            for _ in range(2**n_bits):
                if matriz[k][-j:].count(bit_actual) == j:
                    matriz[k].append(1^bit_actual)
                    bit_actual = 1^bit_actual
                else:
                    matriz[k].append(bit_actual)
        for v in range(len(matriz[0])):
            exprecion = []
            for i in range(len(matriz)):
                exprecion.append(matriz[i][v])
            if compuerta == "AND":
                tdv[str(exprecion)] = True if exprecion.count(1) == n_bits else False
            if compuerta == "OR":
                tdv[str(exprecion)] = True if exprecion.count(1) >= 1 else False
            if compuerta == "NOT":
                tdv[str(exprecion)] = not exprecion[0]
        return tdv
    
    def buscar(self):
        import json
        correct = False
        pesos_sinapticos = []
        actual_epoch = 0
        while actual_epoch < self.epoch and not correct:
            self.pesos_sinapticos = [round(random.random()*20-10) for _ in range(self.n_bits)]
            self.umbral = round(random.random()*20-10)
            for k, j in self.tdv.items():
                suma = 0
                for i, bit in enumerate(json.loads(k)):
                    suma += bit*self.pesos_sinapticos[i]
                result = True if suma > self.umbral else False
                if result == self.tdv[k]:
                    correct = True
                else:
                    correct = False
                    break
            actual_epoch += 1
        return correct, actual_epoch
    
    def entrenar(self):
        result, actual_epoch = self.buscar()
        if result:
            print('APRENDIZAJE EXITOSO EN EL INTENTO: {}'.format(actual_epoch))
            print('Valor del Umbral: {}'.format(self.umbral))
            print('Valor de los Pesos: {}'.format(self.pesos_sinapticos))
        else:
            print('APRENDIZAJE NO EXITOSO EN LOS INTENTOS: {}'.format(actual_epoch))
            print('Valor del Umbral: {}'.format(self.umbral))
            print('Valor de los Pesos: {}'.format(self.pesos_sinapticos))
            
    def evaluar(self, bits = []):
        if len(bits) != self.n_bits:
            print('La cantidad de bits ingresada no es igual a el numero de bits entrenados')
        else:
            try:
                suma = 0
                for i, bit in enumerate(bits):
                    suma += bit* self.pesos_sinapticos[i]
                result = True if suma > self.umbral else False
            except IndexError:
                raise IndexError('La neurona no ha podido ser entrenada')
            return result