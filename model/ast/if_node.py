from model.ast.node import Node

class IfNode(Node):
    def __init__(self, condicion, then_block, else_block=None):
        self.condicion = condicion
        self.then_block = then_block
        self.else_block = else_block
