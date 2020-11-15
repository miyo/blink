import sexpdata

from . import errors
from . import data

def parse_port(lst):
    v = lst.value()
    if(len(v) % 2 == 1):
        raise errors.BlinkParsingError
    ret = []
    for i in range(len(v)//2):
        iomap = data.IOMAP(v[2*i].value())
        if type(v[2*i+1]) is sexpdata.Symbol:
            iomap.pin = v[2*i+1].value()
        else:
            iomap.pin = v[2*i+1][0].value()
            iomap.iostd = v[2*i+1][1]
        ret.append(iomap)
    return ret

def parse_period(lst):
    v = lst.value()
    if(len(v) % 2 == 1):
        raise errors.BlinkParsingError
    ret = {}
    for i in range(len(v)//2):
        ret[v[2*i].value()] = v[2*i+1]
    return ret

def parse_L(lst):
    if(lst[0] != sexpdata.Symbol('L') or len(lst) < 2):
        raise errors.BlinkParsingError
    ret = data.Counter(lst[1])
    lst = lst[2:]
    while(len(lst) > 0):
        if(lst[0] == sexpdata.Symbol(':init') and len(lst) >= 2):
            ret.init = lst[1]
            lst = lst[2:]
        elif(lst[0] == sexpdata.Symbol(':synth-tool') and len(lst) >= 2):
            ret.synth_tool = lst[1]
            lst = lst[2:]
        elif(lst[0] == sexpdata.Symbol(':device') and len(lst) >= 2):
            ret.device = lst[1]
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':at') and len(lst) >= 2):
            ret.at = parse_list(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':iomap') and len(lst) >= 2):
            ret.port = parse_port(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':period') and len(lst) >= 2):
            ret.period = parse_period(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':out') and len(lst) >= 2):
            if type(lst[1]) is sexpdata.Symbol:
                ret.out = data.Port(lst[1].value(), global_port=True)
            elif type(lst[1]) is sexpdata.Quoted:
                ret.out = data.Port(lst[1].value(), global_port=True)
            lst = lst[2:]
        else:
            lst = lst[1:]
    return ret

def parse_list(lst):
    if(lst[0] == sexpdata.Symbol('L')):
        ret = parse_L(lst)
        return ret
    else:
        raise errors.BlinkParsingError


def parse_sexp(s):
    lst = sexpdata.loads(s)
    return parse_list(lst)
    

def parse_source(s):
    s = s.strip()
    ret = data.Counter(64) if s == 'L' else parse_sexp(s)
    print(ret)
    return ret
