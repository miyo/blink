import io
import os
import sys

from . import generator
from . import parser


def parse_file(file):
    name = os.path.splitext(os.path.basename(file))[0]
    with open(file) as f:
        expr = parser.parse_source(f.read())
        ss = io.StringIO()
        generator.generate_counter_module(ss, expr, name)
        with open(name+".v", "w") as g:
            print(ss.getvalue(), file=g)
        
        ss = io.StringIO()
        generator.generate_testbench_module(ss, expr, name)
        with open("tb_"+name+".v", "w") as g:
            print(ss.getvalue(), file=g)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        parse_file(arg)
