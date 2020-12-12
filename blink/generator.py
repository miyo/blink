import io
import math

from . import data

def has_condition(expr):
    return expr.at is not None


def has_specified_output_port(expr):
    return expr.port.global_port


def gen_nested_module_name(n):
    return "{}_{}".format(n, "c")


def gen_bitwidth(value):
    return math.floor(math.log2(value)) + 1 if value > 0 else 1

def generate_throghout_ports(dest, children_info):
    for c in filter(lambda c: c.global_port, children_info.get('outport', [])):
        print('  output wire {},'.format(c.name), file=dest)


def gen_children_sig(children_info, expr):
    ret = []
    for c in filter(lambda c: c.global_port, children_info.get('outport', [])):
        ret.append(c.name)
    if has_condition(expr) and children_info['outport'][-1].global_port == False:
        ret.append(children_info['outport'][-1].name)
    return ret


def generate_children_receivers(dest, children_info, expr):
    for c in filter(lambda c: c.global_port, children_info.get('outport', [])):
        print('  wire {}_w;'.format(c.name), file=dest)
        print('  reg {}_d = 0;'.format(c.name), file=dest)
        print('  assign {0} = {0}_d;'.format(c.name), file=dest)
    if has_condition(expr) and children_info['outport'][-1].global_port == False:
        print('  wire {}_w;'.format(children_info['outport'][-1].name), file=dest)
        print('  reg {}_d = 0;'.format(children_info['outport'][-1].name), file=dest)

    candidates = gen_children_sig(children_info, expr)
    if len(candidates) > 0:
        print('  always @(posedge CLOCK) begin', file=dest)
        print('    if(RESET == 1) begin', file=dest)
        for c in candidates:
            print('      {}_d <= 0;'.format(c), file=dest)
        print('    end else begin', file=dest)
        for c in candidates:
            print('      {0}_d <= {0}_w;'.format(c), file=dest)
        print('    end', file=dest)
        print('  end', file=dest)

def gen_wire(port):
    if port.vector == False:
        return "wire {}".format(port.name)
    else:
        return "wire [{}-1:0] {}".format(port.width, port.name)

def generate_counter_module(dest, expr, name):
    value = expr.value-1 # 0-origin
    
    bitwidth = gen_bitwidth(value)
    initvalue = expr.init
    outport = expr.port
    
    children_info = {}
    if has_condition(expr):
        children_info = generate_counter_module(dest, expr.at, gen_nested_module_name(name))
        
    print('module bl_{}'.format(name), file=dest)
    print('(', file=dest)
    print('  input wire CLOCK,', file=dest)
    print('  input wire RESET,', file=dest)

    generate_throghout_ports(dest, children_info)
        
    print('  output {}'.format(gen_wire(outport)), file=dest)
    print(');', file=dest)
    if(outport.vector == False):
        print("  reg flag = {};".format(initvalue), file=dest)
        print('  assign {} = flag;'.format(outport.name), file=dest)

    generate_children_receivers(dest, children_info, expr)
    
    if value >= 0:
        print('  reg [{}-1:0] counter;'.format(bitwidth), file=dest)
        if(outport.vector):
            print('  assign {} = counter[{}:{}];'.format(outport.name, outport.upper, outport.lower), file=dest)
        
        # ALWAYS BLOCK
        print('  always @(posedge CLOCK) begin', file=dest)

        # RESET
        print('    if(RESET == 1) begin', file=dest)
        print("      counter <= {}'d0;".format(bitwidth), file=dest)
        if(outport.vector == False):
            print('      flag <= {};'.format(initvalue), file=dest)

        # BODY
        print('    end else begin', file=dest)
        indent=""
        if has_condition(expr):
            print('      if({0}_d != {0}_w && {0}_d == 0) begin'.format(children_info['outport'][-1].name), file=dest)
            indent = "  "
        print("      {}if(counter < {}'d{}) begin".format(indent, bitwidth, value), file=dest)
        print("        {}counter <= counter + {}'d1;".format(indent, bitwidth), file=dest)
        print('      {}end else begin'.format(indent), file=dest)
        print('        {}counter <= 0;'.format(indent), file=dest)
        if(outport.vector == False):
            print('        {}flag <= ~flag;'.format(indent), file=dest)
        print('      {}end'.format(indent), file=dest)
        if has_condition(expr):
            print('      end', file=dest)
        print('    end', file=dest)
        print('  end', file=dest)
    elif has_condition(expr):
        print('  always @(posedge CLOCK) begin', file=dest)
        print('    if(RESET == 1) begin', file=dest)
        print('      flag <= {};'.format(initvalue), file=dest)
        print('    end else begin', file=dest)
        print('      flag <= {}_w;'.format(children_info['outport'][-1].name), file=dest)
        print('    end', file=dest)
        print('  end', file=dest)
        
        
    if has_condition(expr):
        connections = [".CLOCK(CLOCK)", ".RESET(RESET)"]
        for c in gen_children_sig(children_info, expr):
            connections.append(".{0}({0}_w)".format(c))
        print('  bl_{0} {0}_inst('.format(gen_nested_module_name(name)), file=dest)
        print('    {}'.format(",".join(connections)), file=dest)
        print('  );', file=dest)
        
    print('endmodule // {}'.format(name), file=dest)
    
    l = children_info.get('outport', [])
    l.append(outport)
    children_info['outport'] = l # update
    return children_info

def generate_testbench_module(dest, expr, name, info):
    print('module tb_{}'.format(name), file=dest)
    print('(', file=dest)
    print(');', file=dest)
    
    print('  reg clk = 0;', file=dest)
    print('  always begin', file=dest)
    print('    #1 clk = ~clk;', file=dest)
    print('  end', file=dest)
    
    print('  reg reset;', file=dest)
    print('  initial begin', file=dest)
    print('    $dumpfile("{}.vcd");'.format(name), file=dest)
    print('    $dumpvars(0);', file=dest)
    print('    reset = 1;', file=dest)
    print('    repeat(10) @(posedge clk);', file=dest)
    print('    reset <= 0;', file=dest)
    if isinstance(expr, data.Counter):
        print('    repeat({}) @(posedge clk);'.format(int(expr.value)*8), file=dest)
    else:
        print('    repeat(100000) @(posedge clk);', file=dest)
    print('    $finish;', file=dest)
    print('  end', file=dest)
    
    connections = [".CLOCK(clk)", ".RESET(reset)"]
    for c in info.get('outport', []):
        if(c.global_port):
            if c.vector:
                print("  wire [{}-1:0] {}_w;".format(c.width, c.name), file=dest)
            else:
                print("  wire {}_w;".format(c.name), file=dest)
            connections.append(".{0}({0}_w)".format(c.name))
    if info.get('outport', [])[-1].global_port == False:
        c = info.get('outport', [])[-1]
        if c.vector:
            print("  wire [{}-1:0] {}_w;".format(c.width, c.name), file=dest)
        else:
            print("  wire {}_w;".format(c.name), file=dest)
        connections.append(".{0}({0}_w)".format(c.name))
    print('  bl_{0} {0}_inst('.format(name), file=dest)
    print('    {}'.format(",".join(connections)), file=dest)
    print('  );', file=dest)

    print('endmodule', file=dest)


def generate_quartus_qsf(dest, expr, name):
    device = expr.device
    family = "Cyclone V"
    if(device.startswith("5C")):
        family = "Cyclone V"
        
    print("set_global_assignment -name FAMILY \"{}\"".format(family), file=dest)
    print("set_global_assignment -name DEVICE {}".format(device), file=dest)
    print("set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files", file=dest)
    print("set_global_assignment -name TOP_LEVEL_ENTITY bl_{}".format(name), file=dest)
    print('set_global_assignment -name VERILOG_FILE {}.v'.format(name), file=dest)
    for p in expr.iomap:
        print("set_location_assignment PIN_{} -to {}".format(p.pin, p.name), file=dest)
        if p.iostd is not None:
            print('set_instance_assignment -name IO_STANDARD "{}" -to {}'.format(p.iostd, p.name), file=dest)
    if expr.period is not None:
        print("set_global_assignment -name SDC_FILE {}.sdc".format(name), file=dest)


def generate_quartus_qpf(dest, name):
    print("PROJECT_REVISION = {}".format(name), file=dest)

        
def generate_quartus_sdc(dest, expr):
    print("set_time_format -unit ns -decimal_places 3", file=dest)
    for p in expr.period.items():
        s = p[0]
        v = float(p[1])
        v0 = '{:.3f}'.format(v)
        v1 = '{:.3f}'.format(v/2)
        print("create_clock -name clk_"+s, "-period {"+v0+"} -waveform {0.000 "+v1+"}", "[get_ports {"+s+"}]", file=dest)


def generate(name, expr):
    ss = io.StringIO()
    info = generate_counter_module(ss, expr, name)
    with open(name+".v", "w") as g:
        print(ss.getvalue(), file=g)
        
    ss = io.StringIO()
    generate_testbench_module(ss, expr, name, info)
    with open("tb_"+name+".v", "w") as g:
        print(ss.getvalue(), file=g)

    if expr.synth_tool is None:
        return
        
    if(expr.synth_tool == "QUARTUS"):
        with open(name+".qsf", "w") as g:
            generate_quartus_qsf(g, expr, name)
        with open(name+".qpf", "w") as g:
            generate_quartus_qpf(g, name)
        with open(name+".sdc", "w") as g:
            generate_quartus_sdc(g, expr)
