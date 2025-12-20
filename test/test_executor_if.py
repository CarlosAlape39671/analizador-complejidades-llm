from model.execution.executor import Executor
from model.ast.program_node import ProgramNode
from model.ast.assignment_node import AssignmentNode
from model.ast.if_node import IfNode
from model.ast.literal_node import LiteralNode


def test_if_then():
    # if 1 then x := 10 end
    ast = ProgramNode([
        IfNode(
            condicion=LiteralNode("1"),
            thenBlock=[
                AssignmentNode("x", LiteralNode("10"))
            ],
            elseBlock=[]
        )
    ])

    executor = Executor()
    env = executor.ejecutar(type("AST", (), {"raiz": ast}))

    assert env.obtener("x") == 10
    
def test_if_else():
    # if 0 then x := 1 else x := 2 end
    ast = ProgramNode([
        IfNode(
            condicion=LiteralNode("0"),
            thenBlock=[
                AssignmentNode("x", LiteralNode("1"))
            ],
            elseBlock=[
                AssignmentNode("x", LiteralNode("2"))
            ]
        )
    ])

    executor = Executor()
    env = executor.ejecutar(type("AST", (), {"raiz": ast}))

    assert env.obtener("x") == 2
