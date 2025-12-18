# model/parser/parser.py

from model.lexer.token_type import TokenType
from model.parser.parse_error import ParseError
from model.ast.ast import AST
from model.ast.program_node import ProgramNode
from model.ast.assignment_node import AssignmentNode
from model.ast.identifier_node import IdentifierNode
from model.ast.literal_node import LiteralNode
from model.ast.binary_expression_node import BinaryExpressionNode
from model.ast.if_node import IfNode
from model.ast.while_node import WhileNode




class Parser:
    """
    Analizador sintáctico descendente recursivo.
    Construye un AST a partir de una lista de tokens.
    """

    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.errores = []

    # =========================
    # API pública
    # =========================

    def parse(self, tokens):
        """
        Punto de entrada del parser.
        Retorna un AST si el código es válido.
        """
        self.tokens = tokens
        self.pos = 0
        self.errores = []

        program = self.parse_program()

        if self.errores:
            return None

        return AST(program)

    def obtenerErrores(self):
        return self.errores

    # =========================
    # Reglas principales
    # =========================

    def parse_program(self):
        """
        program -> statement*
        """
        sentencias = []

        while not self._es_fin():
            stmt = self.parse_statement()
            if stmt is not None:
                sentencias.append(stmt)
            else:
                self._sincronizar()

        return ProgramNode(sentencias)

    def parse_statement(self):
        """
        statement -> assignment | if_statement
        """
        token = self._actual()

        if token.type == TokenType.KEYWORD_IF:
            return self.parse_if()
        
        if token.type == TokenType.KEYWORD_WHILE:
            return self.parse_while()

        if token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()

        self._error(token, "Sentencia no reconocida")
        return None

    def parse_assignment(self):
        """
        assignment -> IDENTIFIER ASSIGN expression
        """
        identificador = self._consumir(
            TokenType.IDENTIFIER, "Se esperaba un identificador"
        )

        self._consumir(
            TokenType.ASSIGN, "Se esperaba el operador de asignación '='"
        )

        expresion = self.parse_expression()

        return AssignmentNode(
            identificador.lexema,
            expresion
        )

    # =========================
    # Expresiones
    # =========================

    def parse_expression(self):
        """
        expression -> comparison
        """
        return self.parse_comparison()

    def parse_comparison(self):
        """
        comparison ->
            arithmetic ((LT | GT | LE | GE | EQ | NEQ) arithmetic)*
        """
        expr = self.parse_arithmetic()

        while self._coincide(
            TokenType.LT,
            TokenType.GT,
            TokenType.LE,
            TokenType.GE,
            TokenType.EQ,
            TokenType.NEQ
        ):
            operador = self._anterior().type
            derecha = self.parse_arithmetic()
            expr = BinaryExpressionNode(operador, expr, derecha)

        return expr

    def parse_arithmetic(self):
        """
        arithmetic -> term ( (PLUS | MINUS) term )*
        """
        expr = self.parse_term()

        while self._coincide(TokenType.PLUS, TokenType.MINUS):
            operador = self._anterior().type
            derecha = self.parse_term()
            expr = BinaryExpressionNode(operador, expr, derecha)

        return expr
    
    def parse_term(self):
        """
        term -> factor ( (MULT | DIV | MOD) factor )*
        """
        expr = self.parse_factor()

        while self._coincide(TokenType.MULT, TokenType.DIV, TokenType.MOD):
            operador = self._anterior().type
            derecha = self.parse_factor()
            expr = BinaryExpressionNode(operador, expr, derecha)

        return expr

    def parse_factor(self):
        """
        factor -> NUMBER | IDENTIFIER | '(' expression ')'
        """
        token = self._actual()

        if self._coincide(TokenType.NUMBER):
            return LiteralNode(token.lexema)

        if self._coincide(TokenType.IDENTIFIER):
            return IdentifierNode(token.lexema)

        if self._coincide(TokenType.LPAREN):
            expr = self.parse_expression()
            self._consumir(TokenType.RPAREN, "Se esperaba ')'")
            return expr

        self._error(token, "Expresión inválida")
        return LiteralNode("0")
    
    def parse_if(self):
        """
        if_statement ->
            IF expression THEN statement*
            (ELSE statement*)?
            END
        """

        # consumir 'if'
        self._consumir(
            TokenType.KEYWORD_IF,
            "Se esperaba 'if'"
        )

        # condición
        condicion = self.parse_expression()

        # consumir 'then'
        self._consumir(
            TokenType.KEYWORD_THEN,
            "Se esperaba 'then'"
        )

        then_block = []

        while (
            not self._verificar(TokenType.KEYWORD_ELSE)
            and not self._verificar(TokenType.KEYWORD_END)
            and not self._es_fin()
        ):
            stmt = self.parse_statement()
            if stmt is not None:
                then_block.append(stmt)
            else:
                self._sincronizar()

        else_block = []

        # else opcional
        if self._coincide(TokenType.KEYWORD_ELSE):
            while (
                not self._verificar(TokenType.KEYWORD_END)
                and not self._es_fin()
            ):
                stmt = self.parse_statement()
                if stmt is not None:
                    else_block.append(stmt)
                else:
                    self._sincronizar()

        # consumir 'end'
        self._consumir(
            TokenType.KEYWORD_END,
            "Se esperaba 'end' al final del if"
        )

        return IfNode(
            condicion=condicion,
            thenBlock=then_block,
            elseBlock=else_block
        )

    def parse_while(self):
        """
        while_stmt -> WHILE expression BEGIN statement* END
        """
        self._consumir(
            TokenType.KEYWORD_WHILE,
            "Se esperaba la palabra clave 'while'"
        )

        condicion = self.parse_expression()

        self._consumir(
            TokenType.KEYWORD_BEGIN,
            "Se esperaba 'begin' para iniciar el bloque del while"
        )

        cuerpo = []

        while not self._verificar(TokenType.KEYWORD_END) and not self._es_fin():
            stmt = self.parse_statement()
            if stmt is not None:
                cuerpo.append(stmt)
            else:
                self._sincronizar()

        self._consumir(
            TokenType.KEYWORD_END,
            "Se esperaba 'end' para cerrar el bloque del while"
        )

        return WhileNode(condicion, cuerpo)


    # =========================
    # Utilidades internas
    # =========================

    def _coincide(self, *tipos):
        for tipo in tipos:
            if self._verificar(tipo):
                self._avanzar()
                return True
        return False

    def _consumir(self, tipo, mensaje):
        if self._verificar(tipo):
            return self._avanzar()

        self._error(self._actual(), mensaje)
        return self._avanzar()

    def _verificar(self, tipo):
        if self._es_fin():
            return False
        return self._actual().type == tipo

    def _avanzar(self):
        if not self._es_fin():
            self.pos += 1
        return self._anterior()

    def _es_fin(self):
        return self.pos >= len(self.tokens)

    def _actual(self):
        if self._es_fin():
            return self.tokens[-1]
        return self.tokens[self.pos]

    def _anterior(self):
        return self.tokens[self.pos - 1]

    def _error(self, token, mensaje):
        self.errores.append(
            ParseError(
                token.linea,
                mensaje,
                token.lexema
            )
        )

    def _sincronizar(self):
        """
        Recuperación básica de errores.
        Avanza hasta encontrar un punto seguro.
        """
        self._avanzar()

        while not self._es_fin():
            if self._anterior().type == TokenType.END:
                return

            self._avanzar()

