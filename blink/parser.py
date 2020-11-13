import sexpdata

def parse_list(lst):
    ret = {}
    while(len(lst) > 0):
        if(lst[0] == sexpdata.Symbol('L') and len(lst) >= 2):
            ret['value'] = lst[1]
            lst = lst[2:]
    print(ret)
    return ret


def parse_sexp(s):
    lst = sexpdata.loads(s)
    return parse_list(lst)
    

def parse_source(s):
    s = s.strip()
    if s == 'L':
        return {'value' : 64}
    elif s[0] == '(':
        return parse_sexp(s)
