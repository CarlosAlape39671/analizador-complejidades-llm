# model/execution/executor.py

from model.execution.environment import Environment
from model.execution.execution_trace import ExecutionTrace

from model.ast.program_node import ProgramNode
from model.ast.assignment_node import AssignmentNode
from model.ast.if_node import IfNode
from model.ast.while_node import WhileNode
from model.ast.for_node import ForNode
from model.ast.repeat_node import RepeatNode
from model.ast.binary_expression_node import BinaryExpressionNode
from model.ast.literal_node import LiteralNode
from model.ast.identifier_node import IdentifierNode


class Executor:
    """
    Intérprete del AST.
    Ejecuta programas completos o paso a paso.
    """

    def __init__(self):
        self.trazas = []
        self.indiceActual = 0

    def ejecutar(self, ast):
        """
        Ejecuta el programa completo.
        """
        env = Environment()
        self.ejecutarNodo(ast.raiz, env)
        return env

    def ejecutarNodo(self, node, env):
        if isinstance(node, ProgramNode):
            for stmt in node.sentencias:
                self.ejecutarNodo(stmt, env)

        elif isinstance(node, AssignmentNode):
            valor = self.evaluar(node.expresion, env)
            env.definir(node.identificador, valor)

        elif isinstance(node, IfNode):
            condicion = self.evaluar(node.condicion, env)
            if condicion:
                for stmt in node.thenBlock:
                    self.ejecutarNodo(stmt, env)
            else:
                for stmt in node.elseBlock:
                    self.ejecutarNodo(stmt, env)

        elif isinstance(node, WhileNode):
            while self.evaluar(node.condicion, env):
                for stmt in node.cuerpo:
                    self.ejecutarNodo(stmt, env)

        elif isinstance(node, ForNode):
            inicio = self.evaluar(node.inicio, env)
            fin = self.evaluar(node.fin, env)

            env.definir(node.variable, inicio)

            while env.obtener(node.variable) <= fin:
                for stmt in node.cuerpo:
                    self.ejecutarNodo(stmt, env)

                env.definir(
                    node.variable,
                    env.obtener(node.variable) + 1
                )

        elif isinstance(node, RepeatNode):
            while True:
                for stmt in node.cuerpo:
                    self.ejecutarNodo(stmt, env)
                if self.evaluar(node.condicion, env):
                    break

    def evaluar(self, expr, env):
        if isinstance(expr, LiteralNode):
            return int(expr.valor)

        if isinstance(expr, IdentifierNode):
            return env.obtener(expr.nombre)

        if isinstance(expr, BinaryExpressionNode):
            izq = self.evaluar(expr.izquierda, env)
            der = self.evaluar(expr.derecha, env)

            op = expr.operador

            if op.name == "PLUS":
                return izq + der
            if op.name == "MINUS":
                return izq - der
            if op.name == "MULT":
                return izq * der
            if op.name == "DIV":
                return izq // der
            if op.name == "MOD":
                return izq % der

            if op.name == "LT":
                return izq < der
            if op.name == "GT":
                return izq > der
            if op.name == "LE":
                return izq <= der
            if op.name == "GE":
                return izq >= der
            if op.name == "EQ":
                return izq == der
            if op.name == "NEQ":
                return izq != der

        raise RuntimeError("Expresión no soportada")
    
    def ejecutarPasoAPaso(self, ast):
        """
        Ejecuta el programa generando trazas paso a paso.
        """
        self.trazas = []
        self.indiceActual = 0

        env = Environment()
        self._ejecutarNodoConTraza(ast.raiz, env)

        return self.trazas

    def _ejecutarNodoConTraza(self, node, env):
        """
        Ejecuta un nodo y registra trazas.
        """

        # Registrar traza ANTES de ejecutar
        self.trazas.append(
            ExecutionTrace(
                linea=getattr(node, "linea", -1),
                accion=type(node).__name__,
                snapshot=self._clonarEnv(env)
            )
        )

        if isinstance(node, ProgramNode):
            for stmt in node.sentencias:
                self._ejecutarNodoConTraza(stmt, env)

        elif isinstance(node, AssignmentNode):
            valor = self.evaluar(node.expresion, env)
            env.definir(node.identificador, valor)

        elif isinstance(node, IfNode):
            condicion = self.evaluar(node.condicion, env)
            bloque = node.thenBlock if condicion else node.elseBlock
            for stmt in bloque:
                self._ejecutarNodoConTraza(stmt, env)

        elif isinstance(node, WhileNode):
            while self.evaluar(node.condicion, env):
                for stmt in node.cuerpo:
                    self._ejecutarNodoConTraza(stmt, env)

        elif isinstance(node, ForNode):
            inicio = self.evaluar(node.inicio, env)
            fin = self.evaluar(node.fin, env)

            env.definir(node.variable, inicio)

            while env.obtener(node.variable) <= fin:
                for stmt in node.cuerpo:
                    self._ejecutarNodoConTraza(stmt, env)
                env.definir(node.variable, env.obtener(node.variable) + 1)

        elif isinstance(node, RepeatNode):
            while True:
                for stmt in node.cuerpo:
                    self._ejecutarNodoConTraza(stmt, env)
                if self.evaluar(node.condicion, env):
                    break

    def _clonarEnv(self, env):
        copia = Environment(env.parent)
        copia.tabla = env.tabla.copy()
        return copia

    def siguientePaso(self):
        if self.indiceActual < len(self.trazas):
            traza = self.trazas[self.indiceActual]
            self.indiceActual += 1
            return traza
        return None

    def pasoAnterior(self):
        if self.indiceActual > 0:
            self.indiceActual -= 1
            return self.trazas[self.indiceActual]
        return None

    def reiniciarPasoAPaso(self):
        self.indiceActual = 0

    def reiniciarEjecucion(self):
        self.trazas = []
        self.indiceActual = 0

