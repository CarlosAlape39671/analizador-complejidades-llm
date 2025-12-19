from model.ast.node import Node


class ForNode(Node):
    def __init__(self, variable, inicio, fin, cuerpo):
        self.variable = variable
        self.inicio = inicio
        self.fin = fin
        self.cuerpo = cuerpo