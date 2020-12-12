
class Module:
    def __init__(self):
        self.synth_tool = None
        self.device = "5CEBA4F23C7"
        self.iomap = []
        self.period = {}

    def __repr__(self):
        h = {'synth_tool':self.synth_tool,
             'device':self.device,
             'iomap':self.iomap,
             }
        return str(h)
    
    def __eq__(self, other):
        if not isinstance(other, Module):
            return False
        return (self.synth_tool == other.synth_tool and
                self.device == other.device and
                self.iomap == other.iomap)

class Port:
    
    def __init__(self, name, global_port=False, vector=False, upper=0, lower=0):
        self.name = name
        self.global_port = global_port
        self.vector = vector
        self.upper = upper
        self.lower = lower
        self.width = upper - lower + 1

    def __repr__(self):
        info = {'name':self.name,
                'global_port':self.global_port,
                'vector':self.vector,
                'uppser':self.upper,
                'lower':self.lower,
                'width':self.width,
        }
        return "Port({})".format(info)

    def __eq__(self, other):
        if not isinstance(other, Port):
            return False
        return (self.name == other.name and
                self.global_port == other.global_port and
                self.vector == other.vector and
                self.upper == other.upper and
                self.lower == other.lower and
                self.width == other.width)


class IOMAP:
    
    def __init__(self, name, pin=None, iostd=None):
        self.name = name
        self.pin = pin
        self.iostd = iostd

    def __repr__(self):
        info = {'name':self.name,
                'pin':self.pin,
                'iostd':self.iostd,
        }
        return "IOMAP({})".format(info)

    def __eq__(self, other):
        if not isinstance(other, IOMAP):
            return False
        return (self.name == other.name and
                self.pin == other.pin and
                self.iostd == other.iostd)


class Counter(Module):

    def __init__(self, value, init=0, port=Port('Q'), at=None):
        super().__init__()
        self.value = value
        self.init = init
        self.port = port
        self.at = at

    def __repr__(self):
        info = {'value':self.value,
                'init':self.init,
                'at':self.at,
                'period':self.period,
                'port':self.port,
        }
        s = "Counter({}".format(info)
        if self.synth_tool is not None:
            s += super().__repr__()
        s += ")"
        return s

    
    def __eq__(self, other):
        if super().__eq__(other) == False:
            return False
        if not isinstance(other, Counter):
            return False
        return (self.value == other.value and
                self.init == other.init and
                self.at == other.at and
                self.period == other.period and
                self.port == other.port)


class InputSwitch(Module):

    def __init__(self, port=Port('S')):
        super().__init__()
        self.port = port

    def __repr__(self):
        info = {'port':self.port,
        }
        s = "Switch({}".format(info)
        if self.synth_tool is not None:
            s += super().__repr__()
        s += ")"
        return s

    
    def __eq__(self, other):
        if super().__eq__(other) == False:
            return False
        if not isinstance(other, Counter):
            return False
        return (self.port == other.port)

class MapValue(Module):

    def __init__(self, value, port=Port('M')):
        super().__init__()
        self.value = value
        self.table = {}

    def __repr__(self):
        info = {'value':self.value,
                'table':self.table,
        }
        s = "Map({}".format(info)
        if self.synth_tool is not None:
            s += super().__repr__()
        s += ")"
        return s

    
    def __eq__(self, other):
        if super().__eq__(other) == False:
            return False
        if not isinstance(other, MapValue):
            return False
        return (self.value == other.value and self.table == other.table)
    
