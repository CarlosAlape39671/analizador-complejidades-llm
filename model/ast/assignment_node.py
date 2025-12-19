from model.ast.node import Node


class AssignmentNode(Node):
    def __init__(self, identificador, expresion):
        self.identificador = identificador
        self.expresion = expresion
