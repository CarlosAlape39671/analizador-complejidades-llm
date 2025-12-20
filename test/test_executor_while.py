from model.ast.assignment_node import AssignmentNode
from model.ast.literal_node import LiteralNode
from model.ast.program_node import ProgramNode
from model.ast.while_node import WhileNode
from model.ast.binary_expression_node import BinaryExpressionNode
from model.execution.executor import Executor
from model.lexer.token_type import TokenType
from model.ast.identifier_node import IdentifierNode


def test_while_loop():
    # x := 0
    # while x < 3
    #   x := x + 1
    # end

    ast = ProgramNode([
        AssignmentNode("x", LiteralNode("0")),
        WhileNode(
            condicion=BinaryExpressionNode(
                TokenType.LT,
                IdentifierNode("x"),
                LiteralNode("3")
            ),
            cuerpo=[
                AssignmentNode(
                    "x",
                    BinaryExpressionNode(
                        TokenType.PLUS,
                        IdentifierNode("x"),
                        LiteralNode("1")
                    )
                )
            ]
        )
    ])

    executor = Executor()
    env = executor.ejecutar(type("AST", (), {"raiz": ast}))

    assert env.obtener("x") == 3
