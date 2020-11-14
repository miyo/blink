import sexpdata

from . import errors

def parse_port(lst):
    v = lst.value()
    if(len(v) % 2 == 1):
        raise BlinkParsingError
    ret = {}
    for i in range(len(v)//2):
        ret[v[2*i].value()] = v[2*i+1]
    return ret

def parse_period(lst):
    v = lst.value()
    if(len(v) % 2 == 1):
        raise BlinkParsingError
    ret = {}
    for i in range(len(v)//2):
        ret[v[2*i].value()] = v[2*i+1]
    return ret

def parse_L(lst):
    ret = {}
    keywords = ['L', ':init', ':synth-tool', ':device', ':out']
    symbols = [sexpdata.Symbol(k) for k in keywords]
    while(len(lst) > 0):
        if(lst[0] in symbols and len(lst) >= 2):
            v = lst[1].value() if type(lst[1]) is sexpdata.Symbol else lst[1]
            ret[lst[0].value()] = v
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':at') and len(lst) >= 2):
            ret[':at'] = parse_L(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':port') and len(lst) >= 2):
            ret[':port'] = parse_port(lst[1])
            lst = lst[2:]
        elif (lst[0] == sexpdata.Symbol(':period') and len(lst) >= 2):
            ret[':period'] = parse_period(lst[1])
            lst = lst[2:]
        else:
            lst = lst[1:]
    return ret

def parse_list(lst):
    if(lst[0] == sexpdata.Symbol('L')):
        ret = parse_L(lst)
        print(ret)
        return ret
    else:
        raise BlinkParsingError


def parse_sexp(s):
    lst = sexpdata.loads(s)
    return parse_list(lst)
    

def parse_source(s):
    s = s.strip()
    if s == 'L':
        return {'L' : 64}
    elif s[0] == '(':
        return parse_sexp(s)
