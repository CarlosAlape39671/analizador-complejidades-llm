# model/lexer/lexer.py

import re
from typing import List

from model.lexer.token import Token
from model.lexer.token_type import TokenType
from model.parser.parse_error import ParseError


class Lexer:
    """
    Analizador léxico del sistema.
    Convierte una cadena de pseudocódigo en una lista de tokens.
    """

    # Palabras reservadas del lenguaje
    KEYWORDS = {
        "if": TokenType.KEYWORD_IF,
        "then": TokenType.KEYWORD_THEN,
        "else": TokenType.KEYWORD_ELSE,
        "for": TokenType.KEYWORD_FOR,
        "to": TokenType.KEYWORD_TO,
        "while": TokenType.KEYWORD_WHILE,
        "repeat": TokenType.KEYWORD_REPEAT,
        "until": TokenType.KEYWORD_UNTIL,
        "begin": TokenType.KEYWORD_BEGIN,
        "end": TokenType.KEYWORD_END,
    }

    # Especificación de tokens usando expresiones regulares
    TOKEN_REGEX = [
        (TokenType.COMMENT, r"//.*"),
        (TokenType.STRING, r"\".*?\""),
        (TokenType.NUMBER, r"\d+"),
        (TokenType.ASSIGN, r":="),
        (TokenType.LE, r"<="),
        (TokenType.GE, r">="),
        (TokenType.EQ, r"=="),
        (TokenType.NEQ, r"!="),
        (TokenType.LT, r"<"),
        (TokenType.GT, r">"),
        (TokenType.PLUS, r"\+"),
        (TokenType.MINUS, r"-"),
        (TokenType.MULT, r"\*"),
        (TokenType.DIV, r"/"),
        (TokenType.MOD, r"%"),
        (TokenType.LPAREN, r"\("),
        (TokenType.RPAREN, r"\)"),
        (TokenType.COMMA, r","),
        (TokenType.IDENTIFIER, r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ]

    def __init__(self):
        self.errores: List[ParseError] = []

    def tokenizar(self, codigo: str) -> List[Token]:
        """
        Convierte el código fuente en una lista de tokens.
        """
        self.errores.clear()
        tokens: List[Token] = []

        lineas = codigo.splitlines()

        for num_linea, linea in enumerate(lineas, start=1):
            columna = 1
            texto = linea

            while texto:
                texto = texto.lstrip()
                desplazamiento = len(linea) - len(texto)
                columna = desplazamiento + 1

                if not texto:
                    break

                match = None

                for token_type, patron in self.TOKEN_REGEX:
                    regex = re.compile(patron)
                    match = regex.match(texto)
                    if match:
                        lexema = match.group(0)

                        # Identificador o palabra reservada
                        if token_type == TokenType.IDENTIFIER:
                            token_type = self.KEYWORDS.get(
                                lexema.lower(), TokenType.IDENTIFIER
                            )

                        # Ignorar comentarios
                        if token_type != TokenType.COMMENT:
                            tokens.append(
                                Token(token_type, lexema, num_linea, columna)
                            )

                        texto = texto[len(lexema):]
                        break

                if not match:
                    # Error léxico
                    self.errores.append(
                        ParseError(
                            linea=num_linea,
                            mensaje="Símbolo no reconocido",
                            fragmento=texto[0]
                        )
                    )
                    texto = texto[1:]

        return tokens

    def obtenerErrores(self) -> List[ParseError]:
        """
        Retorna la lista de errores léxicos encontrados.
        """
        return self.errores
