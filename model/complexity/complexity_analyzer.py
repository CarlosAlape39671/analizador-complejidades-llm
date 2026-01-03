# model/complexity/complexity_analyzer.py

from model.ast.program_node import ProgramNode
from model.ast.assignment_node import AssignmentNode
from model.ast.if_node import IfNode
from model.ast.while_node import WhileNode
from model.ast.for_node import ForNode
from model.ast.repeat_node import RepeatNode

from model.complexity.complexity_result import ComplexityResult


class ComplexityAnalyzer:
    """
    Analizador de complejidad temporal basado en el AST.
    """

    def analizar(self, ast):
        complejidad = self._analizar_nodo(ast.raiz)

        return ComplexityResult(
            O=complejidad,
            Omega=complejidad,
            Theta=complejidad,
            detalles="Estimación basada en estructura del AST"
        )

    def _analizar_nodo(self, node):
        if isinstance(node, ProgramNode):
            return self._analizar_lista(node.sentencias)

        if isinstance(node, AssignmentNode):
            return "1"

        if isinstance(node, IfNode):
            then_c = self._analizar_lista(node.thenBlock)
            else_c = self._analizar_lista(node.elseBlock)
            return f"max({then_c}, {else_c})"

        if isinstance(node, WhileNode):
            cuerpo = self._analizar_lista(node.cuerpo)
            return f"n * {cuerpo}"

        if isinstance(node, ForNode):
            cuerpo = self._analizar_lista(node.cuerpo)
            return f"n * {cuerpo}"

        if isinstance(node, RepeatNode):
            cuerpo = self._analizar_lista(node.cuerpo)
            return f"n * {cuerpo}"

        return "1"

    def _analizar_lista(self, sentencias):
        if not sentencias:
            return "1"

        partes = [self._analizar_nodo(s) for s in sentencias]

        # Simplificación básica
        if len(partes) == 1:
            return partes[0]

        return " + ".join(partes)
