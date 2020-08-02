#!/usr/bin/python3
#
##################################################################################
# Main
##################################################################################

import simple_lang.simple_lang as sl

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="filename", help="path to SimpleLang file", type=str)
    args = parser.parse_args()
    with open(args.filename) as f:
        src = f.read()
        tokens = sl.Tokenizer(src).tokenize()
        ast = sl.Parser(tokens).parse()
        out = sl.Printer()(ast)
    with open(args.filename, "w") as f:
        f.write(out)
