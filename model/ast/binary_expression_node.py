from model.ast.expression_node import ExpressionNode


class BinaryExpressionNode(ExpressionNode):
    def __init__(self, operador, izquierda, derecha):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha
