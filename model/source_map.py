class SourceMap:
    def __init__(self):
        self.nodo_a_linea = {}
        self.linea_a_nodos = {}

    def registrar(self, nodo, linea):
        # Si el nodo ya estaba registrado, limpiar vínculo anterior
        if nodo in self.nodo_a_linea:
            linea_anterior = self.nodo_a_linea[nodo]
            self.linea_a_nodos[linea_anterior].remove(nodo)

        self.nodo_a_linea[nodo] = linea
        self.linea_a_nodos.setdefault(linea, []).append(nodo)

    def obtenerLinea(self, nodo):
        return self.nodo_a_linea.get(nodo)

    def obtenerNodos(self, linea):
        return self.linea_a_nodos.get(linea, [])

