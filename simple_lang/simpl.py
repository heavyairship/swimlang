#!/usr/bin/python3
#
##################################################################################
# Main
##################################################################################

import simple_lang.simple_lang as sl

import argparse
import sys
sys.setrecursionlimit(10**6)  # FixMe: remove and evaluate iteratively

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="filename", help="path to SimpleLang file", type=str)
    parser.add_argument("-v", "--verbose", dest="verbose",
                        help="run in verbose mode", action='store_true')
    args = parser.parse_args()
    with open(args.filename) as f:
        src = f.read()
        print(sl.Interpreter(src).interpret(verbose=args.verbose))
