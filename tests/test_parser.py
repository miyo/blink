from blink import parser
from blink import data

def test_parse_L():
    l = parser.parse_source("L")
    assert(l == data.Counter(64))
