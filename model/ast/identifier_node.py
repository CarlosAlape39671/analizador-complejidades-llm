from model.ast.expression_node import ExpressionNode


class IdentifierNode(ExpressionNode):
    def __init__(self, nombre):
        self.nombre = nombre
