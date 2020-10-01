#!/usr/bin/python3

from swimlang.tokenizer import Tokenizer
from swimlang.parser import Parser
from swimlang.printer import Printer

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="filename", help="path to swimlang file", type=str)
    args = parser.parse_args()
    with open(args.filename) as f:
        src = f.read()
        tokens = Tokenizer(src).tokenize()
        ast = Parser(tokens).parse()
        out = Printer()(ast)
    with open(args.filename, "w") as f:
        f.write(out)
