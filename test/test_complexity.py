# test/test_complexity.py

from model.complexity.complexity_analyzer import ComplexityAnalyzer
from model.lexer.lexer import Lexer
from model.parser.parser import Parser


def test_complexity_assignment():
    codigo = "x := 5"

    lexer = Lexer()
    parser = Parser()
    analyzer = ComplexityAnalyzer()

    ast = parser.parse(lexer.tokenizar(codigo))
    result = analyzer.analizar(ast)

    assert result.O == "1"

def test_complexity_if():
    codigo = """if x < 5 then
x := 1
else
x := 2
end"""

    lexer = Lexer()
    parser = Parser()
    analyzer = ComplexityAnalyzer()

    ast = parser.parse(lexer.tokenizar(codigo))
    result = analyzer.analizar(ast)

    assert "max" in result.O

def test_complexity_for():
    codigo = """for i := 1 to 10 begin
x := i
end"""

    lexer = Lexer()
    parser = Parser()
    analyzer = ComplexityAnalyzer()

    ast = parser.parse(lexer.tokenizar(codigo))
    result = analyzer.analizar(ast)

    assert "n *" in result.O

def test_complexity_nested_loops():
    codigo = """while x < n begin
while y < n begin
y := y + 1
end
end"""

    lexer = Lexer()
    parser = Parser()
    analyzer = ComplexityAnalyzer()

    ast = parser.parse(lexer.tokenizar(codigo))
    result = analyzer.analizar(ast)

    assert "n * n *" in result.O or "n * n" in result.O

def test_complexity_constant_program():
    codigo = """x := 1
y := 2"""

    lexer = Lexer()
    parser = Parser()
    analyzer = ComplexityAnalyzer()

    ast = parser.parse(lexer.tokenizar(codigo))
    result = analyzer.analizar(ast)

    assert result.O == "1 + 1"

def test_complexity_if_empty():
    codigo = """if x < 5 then
end"""

    lexer = Lexer()
    parser = Parser()
    analyzer = ComplexityAnalyzer()

    ast = parser.parse(lexer.tokenizar(codigo))
    result = analyzer.analizar(ast)

    assert "max" in result.O
