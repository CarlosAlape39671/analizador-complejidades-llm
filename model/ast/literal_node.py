from model.ast.expression_node import ExpressionNode


class LiteralNode(ExpressionNode):
    def __init__(self, valor):
        self.valor = valor
