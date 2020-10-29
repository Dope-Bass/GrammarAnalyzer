# -*- coding: UTF-8 -*-

import sys
import argparse

import c_analyzer


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", default="")

    return parser


if __name__ == '__main__':
    p = create_parser()
    namespace = p.parse_args(sys.argv[1:])

    a = c_analyzer.Analyzer(namespace.text)

    print(a.make_sense())
    a.close()
