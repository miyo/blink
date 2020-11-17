import sexpdata

from blink import parser
from blink import data

def test_parse_L():
    l = parser.parse_source("L")
    assert(l == data.Counter(64))

def test_parse_L():
    l = parser.parse_source("(L 1024 :out '(Q 7 3))")
    assert(l == data.Counter(1024, port=data.Port('Q', global_port=True, vector=True, upper=7, lower=3)))

def test_parse_iomap():
    l = parser.parse_iomap(sexpdata.loads("'(CLOCK M9)"))
    assert(l == [data.IOMAP('CLOCK', pin='M9')])

def test_parse_iomap_2():
    l = parser.parse_iomap(sexpdata.loads("'(CLOCK (M9 \"3.3-V LVTTL\"))"))
    assert(l == [data.IOMAP('CLOCK', pin='M9', iostd='3.3-V LVTTL')])

def test_parse_iomap_3():
    expr = "'(Q ((AA2 \"3.3-V LVTTL\") (AA1 \"3.3-V LVTTL\")))"
    l = parser.parse_iomap(sexpdata.loads(expr))
    assert(l == [data.IOMAP('Q[0]', pin='AA2', iostd='3.3-V LVTTL'),
                 data.IOMAP('Q[1]', pin='AA1', iostd='3.3-V LVTTL'),
                 ])
