from model.execution.executor import Executor
from model.execution.environment import Environment

from model.ast.program_node import ProgramNode
from model.ast.assignment_node import AssignmentNode
from model.ast.literal_node import LiteralNode


def test_assignment_simple():
    # x := 5
    ast = ProgramNode([
        AssignmentNode("x", LiteralNode("5"))
    ])

    executor = Executor()
    env = executor.ejecutar(type("AST", (), {"raiz": ast}))

    assert env.obtener("x") == 5
