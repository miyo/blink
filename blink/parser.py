import sexpdata

from . import errors
from . import data

def parse_iomap(lst):
    v = lst.value()
    if(len(v) % 2 == 1):
        raise errors.BlinkParsingError
    ret = []
    for i in range(len(v)//2):
        if type(v[2*i+1]) is sexpdata.Symbol:
            iomap = data.IOMAP(v[2*i].value())
            iomap.pin = v[2*i+1].value()
            ret.append(iomap)
        else:
            if type(v[2*i+1][0]) is sexpdata.Symbol:
                iomap = data.IOMAP(v[2*i].value())
                iomap.pin = v[2*i+1][0].value()
                iomap.iostd = v[2*i+1][1]
                ret.append(iomap)
            elif type(v[2*i+1][0]) is list:
                for j,x in enumerate(v[2*i+1]):
                    iomap = data.IOMAP("{}[{}]".format(v[2*i].value(), j))
                    iomap.pin = x[0].value()
                    iomap.iostd = x[1]
                    ret.append(iomap)
            else:
                raise errors.BlinkParsingError
    return ret

def parse_port(a):
    if type(a) is sexpdata.Symbol:
        return data.Port(a.value(), global_port=True)
    elif type(a) is sexpdata.Quoted:
        v = a.value()
        if(len(v) == 3 and type(v[1]) is int and type(v[2]) is int):
            return data.Port(v[0].value(), global_port=True, vector=True, upper=v[1], lower=v[2])
        else:
            raise errors.BlinkParsingError
    else:
        raise errors.BlinkParsingError

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
            ret.iomap = parse_iomap(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':period') and len(lst) >= 2):
            ret.period = parse_period(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':out') and len(lst) >= 2):
            ret.port = parse_port(lst[1])
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
    ret = None
    if s == 'L':
        ret = data.Counter(12500000)
        ret.synth_tool = "QUARTUS"
        ret.device = "5CEBA4F23C7"
        ret.iomap = [data.IOMAP("CLOCK", pin="M9"),
                      data.IOMAP("RESET", pin="U13"),
                      data.IOMAP("Q", pin="L1")]
        ret.period = {"CLOCK": "20.0"}
    else:
        ret = parse_sexp(s)
        print(ret)
    return ret
