# -*- coding: UTF-8 -*-

import sys
import argparse

import c_analyzer


"""
    Скрипт для запуска анализатора из командной строки
    
    Как с ним работать написано в README
"""


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", default="")
    parser.add_argument("-f", "--file", default="")

    return parser


if __name__ == '__main__':
    p = create_parser()
    namespace = p.parse_args(sys.argv[1:])

    a = c_analyzer.Analyzer(namespace.text)
    string = ''
    f = ''

    for e in a.make_sense():
        string = string + '{0}'.format(e)

    if namespace.file == 'n':
        print(string)
    elif namespace.file != '':
        f = open(namespace.file, 'w')
    else:
        f = open('res.txt', 'w')

    if f:
        f.write(string)
        f.close()

    # print(a.make_sense())
    a.close()
