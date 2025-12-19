from model.ast.node import Node

class ForNode(Node):
    """
    Representa una estructura FOR en el AST.

    for variable = inicio to fin begin
        cuerpo
    end
    """

    def __init__(self, variable, inicio, fin, cuerpo):
        self.variable = variable          # str
        self.inicio = inicio              # ExpressionNode
        self.fin = fin                    # ExpressionNode
        self.cuerpo = cuerpo              # List[Node]
