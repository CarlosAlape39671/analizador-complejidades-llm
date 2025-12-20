from model.ast.node import Node


class AssignmentNode(Node):
    def __init__(self, identificador, expresion, linea=None):
        super().__init__(linea=identificador.linea)
        self.identificador = identificador
        self.expresion = expresion
