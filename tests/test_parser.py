from blink import parser
from blink import data

def test_parse_L():
    l = parser.parse_source("L")
    assert(l == data.Counter(64))

def test_parse_L():
    l = parser.parse_source("(L 1024 :out '(Q 7 3))")
    assert(l == data.Counter(1024, out=data.Port('Q', global_port=True, vector=True, upper=7, lower=3)))
