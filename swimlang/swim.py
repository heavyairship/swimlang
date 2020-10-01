#!/usr/bin/python3

from swimlang.interpreter import Interpreter

import argparse
import sys
sys.setrecursionlimit(10**6)  # FixMe: remove and evaluate iteratively

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="filename", help="path to swimlang file", type=str)
    parser.add_argument("-v", "--verbose", dest="verbose",
                        help="run in verbose mode", action='store_true')
    args = parser.parse_args()
    with open(args.filename) as f:
        src = f.read()
        print(Interpreter(src).interpret(verbose=args.verbose))
