from model.source_map import SourceMap
from model.ast.assignment_node import AssignmentNode
from model.ast.literal_node import LiteralNode

def test_register_and_get_line():
    source_map = SourceMap()

    nodo = AssignmentNode("x", LiteralNode("5"))
    source_map.registrar(nodo, 3)

    assert source_map.obtenerLinea(nodo) == 3

def test_multiple_nodes_same_line():
    source_map = SourceMap()

    n1 = AssignmentNode("x", LiteralNode("1"))
    n2 = AssignmentNode("y", LiteralNode("2"))

    source_map.registrar(n1, 5)
    source_map.registrar(n2, 5)

    nodos = source_map.obtenerNodos(5)

    assert n1 in nodos
    assert n2 in nodos

def test_unregistered_node():
    source_map = SourceMap()

    nodo = AssignmentNode("x", LiteralNode("10"))

    assert source_map.obtenerLinea(nodo) is None

def test_line_without_nodes():
    source_map = SourceMap()

    nodos = source_map.obtenerNodos(100)

    assert nodos == []

def test_line_without_nodes():
    source_map = SourceMap()

    nodos = source_map.obtenerNodos(100)

    assert nodos == []

def test_override_node_line():
    source_map = SourceMap()

    nodo = AssignmentNode("x", LiteralNode("5"))

    source_map.registrar(nodo, 1)
    source_map.registrar(nodo, 10)

    assert source_map.obtenerLinea(nodo) == 10
