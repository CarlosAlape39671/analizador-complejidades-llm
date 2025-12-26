# tests/test_parser_sourcemap.py

from model.lexer.lexer import Lexer
from model.parser.parser import Parser
from model.ast.assignment_node import AssignmentNode
from model.ast.if_node import IfNode
from model.ast.assignment_node import AssignmentNode
from model.ast.repeat_node import RepeatNode



def test_assignment_linea_y_sourcemap():
    codigo = "x := 5"

    lexer = Lexer()
    parser = Parser()

    tokens = lexer.tokenizar(codigo)
    ast = parser.parse(tokens)

    assert ast is not None

    nodo = ast.raiz.sentencias[0]
    assert isinstance(nodo, AssignmentNode)

    # Línea correcta
    assert nodo.linea == 1

    # SourceMap correcto
    assert ast.sourceMap.obtenerLinea(nodo) == 1

def test_if_lineas_sourcemap():
    codigo = """if x < 5 then
y := 3
end"""

    lexer = Lexer()
    parser = Parser()

    tokens = lexer.tokenizar(codigo)
    ast = parser.parse(tokens)

    if_node = ast.raiz.sentencias[0]
    assert isinstance(if_node, IfNode)

    # IF está en la línea 1
    assert if_node.linea == 1
    assert ast.sourceMap.obtenerLinea(if_node) == 1

    asignacion = if_node.thenBlock[0]
    assert isinstance(asignacion, AssignmentNode)

    # Assignment está en la línea 2
    assert asignacion.linea == 2
    assert ast.sourceMap.obtenerLinea(asignacion) == 2
    
def test_repeat_linea_sourcemap():
    codigo = """repeat
x := x + 1
until x > 5"""

    lexer = Lexer()
    parser = Parser()

    tokens = lexer.tokenizar(codigo)
    ast = parser.parse(tokens)

    repeat_node = ast.raiz.sentencias[0]
    assert isinstance(repeat_node, RepeatNode)

    # Línea del REPEAT
    assert repeat_node.linea == 1
    assert ast.sourceMap.obtenerLinea(repeat_node) == 1

    asignacion = repeat_node.cuerpo[0]
    assert asignacion.linea == 2
    assert ast.sourceMap.obtenerLinea(asignacion) == 2

def test_multiples_sentencias_sourcemap():
    codigo = """x := 1
y := 2
z := x + y"""

    lexer = Lexer()
    parser = Parser()

    tokens = lexer.tokenizar(codigo)
    ast = parser.parse(tokens)

    for i, stmt in enumerate(ast.raiz.sentencias):
        assert stmt.linea == i + 1
        assert ast.sourceMap.obtenerLinea(stmt) == i + 1
