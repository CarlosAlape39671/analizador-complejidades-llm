class Node:
    """
    Nodo base del AST.
    Todos los nodos del lenguaje heredan de esta clase.
    """
    def __init__(self, linea=None):
        self.linea = linea
