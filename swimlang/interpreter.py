##################################################################################
# Interpreter
##################################################################################

from swimlang.tokenizer import Tokenizer
from swimlang.parser import Parser
from swimlang.evaluator import Evaluator
from swimlang.printer import Printer


class Interpreter(object):
    def __init__(self, src):
        self.src = src

    def interpret(self, verbose=False):
        tokens = Tokenizer(self.src).tokenize()
        ast = Parser(tokens).parse()
        if verbose:
            print("\n*********************")
            print("Parsed the following:")
            print("*********************")
            print(Printer()(ast))
            print("*********************\n")
        res = Evaluator()(ast)
        return res
