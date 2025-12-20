from concurrent.futures import Executor
from model.ast.assignment_node import AssignmentNode
from model.ast.for_node import ForNode
from model.ast.identifier_node import IdentifierNode
from model.ast.literal_node import LiteralNode
from model.ast.program_node import ProgramNode


def test_for_loop():
    # for i := 1 to 3
    #   x := i
    # end

    ast = ProgramNode([
        AssignmentNode("x", LiteralNode("0")),
        ForNode(
            variable="i",
            inicio=LiteralNode("1"),
            fin=LiteralNode("3"),
            cuerpo=[
                AssignmentNode("x", IdentifierNode("i"))
            ]
        )
    ])

    executor = Executor()
    env = executor.ejecutar(type("AST", (), {"raiz": ast}))

    assert env.obtener("x") == 3
