from model.ast.node import Node

class RepeatNode(Node):
    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo
