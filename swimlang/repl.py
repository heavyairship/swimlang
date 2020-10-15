##################################################################################
# Read-eval-print-loop
##################################################################################

from swimlang.tokenizer import Tokenizer
from swimlang.parser import Parser
from swimlang.evaluator import Evaluator

import cmd
import sys
import traceback

INIT_PROMPT = "><`> "
CONT_PROMPT = "~~~~ "
STOP = "."
RETURN = "---> "


class Repl(cmd.Cmd):
    intro = """
welcome  to  swim 
><`>  ><`>  ><`> 

type `(exit)` to exit
type `.` and hit enter to finish an expression
"""
    prompt = INIT_PROMPT
    done = False
    buffer = None
    evaluator = Evaluator()

    def precmd(self, line):
        if self.buffer is None and line in ["(exit)", "EOF"]:
            sys.exit()

        # Add back newline since it is a valid separator.
        line += "\n"

        if self.buffer is None:
            self.buffer = line
        else:
            self.buffer += line

        stripped_buffer = self.buffer.strip()
        if len(stripped_buffer) and stripped_buffer[-1] == STOP:
            expr = stripped_buffer[:-1]
            try:
                tokens = Tokenizer(expr).tokenize()
                ast = Parser(tokens).parse()
                res = self.evaluator(ast)
                print(RETURN + str(res))
            except:
                traceback.print_exc()
            finally:
                self.buffer = None
                self.prompt = INIT_PROMPT
        else:
            self.prompt = CONT_PROMPT

        return line

    def default(self, line):
        pass
