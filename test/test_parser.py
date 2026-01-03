# test/test_parser.py

from model.lexer.lexer import Lexer
from model.parser.parser import Parser


def test_parser_empty_program():
    lexer = Lexer()
    parser = Parser()

    ast = parser.parse(lexer.tokenizar(""))
    assert ast is not None
    assert ast.raiz.sentencias == []

def test_parser_syntax_error():
    codigo = "x :="

    lexer = Lexer()
    parser = Parser()

    ast = parser.parse(lexer.tokenizar(codigo))

    assert ast is None
    assert len(parser.obtenerErrores()) > 0

def test_parser_if_without_else():
    codigo = """if x < 5 then
x := 1
end"""

    lexer = Lexer()
    parser = Parser()

    ast = parser.parse(lexer.tokenizar(codigo))

    assert ast is not None
    assert len(ast.raiz.sentencias) == 1

def test_parser_while_empty_body():
    codigo = """while x < 5 begin
end"""

    lexer = Lexer()
    parser = Parser()

    ast = parser.parse(lexer.tokenizar(codigo))
    assert ast is not None
