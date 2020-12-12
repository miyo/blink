import os
import sys

from . import generator
from . import parser


def parse_file(file):
    name = os.path.splitext(os.path.basename(file))[0]
    with open(file) as f:
        expr = parser.parse_source(f.read())
        generator.generate(name, expr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} sources".format(sys.argv[0]))
        exit()
    for arg in sys.argv[1:]:
        parse_file(arg)
