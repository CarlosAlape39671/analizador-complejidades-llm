from model.ast.node import Node


class ProgramNode(Node):
    def __init__(self, sentencias):
        self.sentencias = sentencias
