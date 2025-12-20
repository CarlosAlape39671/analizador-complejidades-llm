from concurrent.futures import Executor
from model.ast.assignment_node import AssignmentNode
from model.ast.binary_expression_node import BinaryExpressionNode
from model.ast.identifier_node import IdentifierNode
from model.ast.literal_node import LiteralNode
from model.ast.program_node import ProgramNode
from model.ast.repeat_node import RepeatNode
from model.lexer.token_type import TokenType


def test_repeat_until():
    # x := 0
    # repeat
    #   x := x + 1
    # until x == 3

    ast = ProgramNode([
        AssignmentNode("x", LiteralNode("0")),
        RepeatNode(
            cuerpo=[
                AssignmentNode(
                    "x",
                    BinaryExpressionNode(
                        TokenType.PLUS,
                        IdentifierNode("x"),
                        LiteralNode("1")
                    )
                )
            ],
            condicion=BinaryExpressionNode(
                TokenType.EQ,
                IdentifierNode("x"),
                LiteralNode("3")
            )
        )
    ])

    executor = Executor()
    env = executor.ejecutar(type("AST", (), {"raiz": ast}))

    assert env.obtener("x") == 3

def test_traces_are_generated():
    ast = ProgramNode([
        AssignmentNode("x", LiteralNode("1"))
    ])

    executor = Executor()
    traces = executor.ejecutarPasoAPaso(type("AST", (), {"raiz": ast}))

    assert len(traces) > 0
    assert traces[0].accion is not None
    assert traces[0].snapshot is not None