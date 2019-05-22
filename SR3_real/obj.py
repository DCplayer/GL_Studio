
class Obj():
    def __init__(self, f):
        self.caras = []
        self.vertex = []

        file = open(f, 'r')
        for line in file:
            linea = line.split(' ')
            if linea[0] == 'v':
                tupla = [linea[1], linea[2], linea[3]]
                self.vertex.append(tupla)
            elif linea[0] == 'f':
                tupla = []
                for i in range(len(linea) -1):
                    tupla.append(linea[i+1])
                self.caras.append(tupla)
            else:
                continue
        print(self.caras)
