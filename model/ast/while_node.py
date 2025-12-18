from model.ast.node import Node

class WhileNode(Node):
    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo