# test/test_executor.py

from model.lexer.lexer import Lexer
from model.parser.parser import Parser
from model.execution.executor import Executor


def test_executor_asignacion_simple():
    codigo = "x := 5"

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    tokens = lexer.tokenizar(codigo)
    ast = parser.parse(tokens)

    trazas = executor.ejecutarPasoAPaso(ast)

    # Debe haber al menos 2 trazas:
    # 1) entrada al nodo
    # 2) asignación
    assert len(trazas) >= 2

    traza = trazas[1]

    assert traza.linea == 1
    assert "Asignación" in traza.accion
    assert traza.snapshot.tabla["x"] == 5

def test_executor_if_true():
    codigo = """x := 1
if x < 5 then
y := 3
end"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    trazas = executor.ejecutarPasoAPaso(ast)

    # Buscar traza del IF
    if_trazas = [t for t in trazas if "IF condición" in t.accion]
    assert len(if_trazas) == 1
    assert if_trazas[0].linea == 2

    # Verificar que y fue asignada
    snapshots = [t.snapshot.tabla for t in trazas]
    assert any("y" in s and s["y"] == 3 for s in snapshots)

def test_executor_while():
    codigo = """x := 0
while x < 3 begin
x := x + 1
end"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    trazas = executor.ejecutarPasoAPaso(ast)

    # Contar iteraciones del while
    iteraciones = [t for t in trazas if "Iteración WHILE" in t.accion]
    assert len(iteraciones) == 3

    # Valor final de x
    assert trazas[-1].snapshot.tabla["x"] == 3
    

def test_executor_for():
    codigo = """for i := 1 to 3 begin
x := i
end"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    trazas = executor.ejecutarPasoAPaso(ast)

    iteraciones = [t for t in trazas if "Iteración FOR" in t.accion]
    assert len(iteraciones) == 3

    # Último valor
    assert trazas[-1].snapshot.tabla["x"] == 3

def test_executor_repeat_until():
    codigo = """x := 0
repeat
x := x + 1
until x == 3"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    trazas = executor.ejecutarPasoAPaso(ast)

    iteraciones = [t for t in trazas if "Iteración REPEAT" in t.accion]
    assert len(iteraciones) == 3

    assert trazas[-1].snapshot.tabla["x"] == 3

def test_siguiente_y_anterior():
    codigo = "x := 5"

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    executor.ejecutarPasoAPaso(ast)

    t1 = executor.siguientePaso()
    t2 = executor.siguientePaso()
    t_back = executor.pasoAnterior()

    assert t_back == t1

def test_executor_assignment():
    codigo = "x := 10"

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    env = executor.ejecutar(ast)

    assert env.obtener("x") == 10

def test_executor_for_loop():
    codigo = """for i := 1 to 3 begin
x := i
end"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    env = executor.ejecutar(ast)

    assert env.obtener("i") == 4
    assert env.obtener("x") == 3

def test_executor_step_by_step():
    codigo = """x := 1
x := x + 1"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))
    trazas = executor.ejecutarPasoAPaso(ast)

    assert len(trazas) >= 2
    assert trazas[0].snapshot.obtener("x") == 1

