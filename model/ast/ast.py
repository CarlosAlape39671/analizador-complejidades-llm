from model.ast.program_node import ProgramNode


class AST:
    """
    Representa el Árbol de Sintaxis Abstracta completo.
    Contiene la raíz del árbol (ProgramNode).
    """

    def __init__(self, raiz: ProgramNode):
        self.raiz = raiz
