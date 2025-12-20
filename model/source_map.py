# model/source_map.py

class SourceMap:
    """
    Mapea nodos del AST a líneas del código fuente.
    Permite saber qué línea ejecutar o resaltar en la vista.
    """

    def __init__(self):
        self.nodoALinea = {}

    def registrar(self, nodo, linea: int):
        """
        Asocia un nodo del AST con una línea del código.
        """
        self.nodoALinea[nodo] = linea

    def obtenerLinea(self, nodo):
        """
        Retorna la línea asociada a un nodo.
        Si no existe, retorna -1.
        """
        return self.nodoALinea.get(nodo, -1)
