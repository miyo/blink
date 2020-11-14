import io
import math

def has_condition(expr):
    return ':at' in expr.keys()

def has_specified_output_port(expr):
    return ':out' in expr.keys()

def gen_nested_module_name(n):
    return "{}_{}".format(n, "c")

def generate_counter_module(dest, expr, name):
    value = expr['L']-1
    
    bitwidth = math.floor(math.log2(value)) + 1 if value > 0 else 1
    initvalue = expr.get(":init", 0)
    outport = expr.get(":out", 'Q')
    
    children_info = {}
    if has_condition(expr):
        children_info = generate_counter_module(dest, expr[':at'], gen_nested_module_name(name))
        
    print('module bl_{}'.format(name), file=dest)
    print('(', file=dest)
    print('  input wire CLOCK,', file=dest)
    print('  input wire RESET,', file=dest)
    for c in children_info.get('outport', []):
        if(c[0]):
            print('  output wire {},'.format(c[1]), file=dest)
        
    print('  output wire {}'.format(outport), file=dest)
    print(');', file=dest)
    print("  reg flag = {};".format(initvalue), file=dest)
    print('  assign {} = flag;'.format(outport), file=dest)
    for c in children_info.get('outport', []):
        if(c[0]):
            print('  wire {}_w;'.format(c[1]), file=dest)
            print('  reg {}_d = 0;'.format(c[1]), file=dest)
            print('  assign {0} = {0}_d;'.format(c[1]), file=dest)
    if has_condition(expr) and children_info['outport'][-1][0] == False:
        o = children_info['outport'][-1][1]
        print('  wire {}_w;'.format(o), file=dest)
        print('  reg {0}_d = 0;'.format(o), file=dest)
    if value >= 0:
        print('  reg [{}-1:0] counter;'.format(bitwidth), file=dest)
        
        # ALWAYS BLOCK
        print('  always @(posedge CLOCK) begin', file=dest)

        # RESET
        print('    if(RESET == 1) begin', file=dest)
        print("      counter <= {}'d0;".format(bitwidth), file=dest)
        print('      flag <= {};'.format(initvalue), file=dest)
        for c in children_info.get('outport', []):
            if(c[0]):
                print('      {}_d <= 0;'.format(c[1]), file=dest)
        if has_condition(expr) and children_info['outport'][-1][0] == False:
            print('      {}_d <= 0;'.format(children_info['outport'][-1][1]), file=dest)

        # BODY
        print('    end else begin', file=dest)
        for c in children_info.get('outport', []):
            print('      {0}_d <= {0}_w;'.format(c[1]), file=dest)
        indent=""
        if has_condition(expr):
            print('      if({0}_d != {0}_w && {0}_w == 1) begin'.format(children_info['outport'][-1][1]), file=dest)
            indent = "  "
        print("      {}if(counter < {}'d{}) begin".format(indent, bitwidth, value), file=dest)
        print("        {}counter <= counter + {}'d1;".format(indent, bitwidth), file=dest)
        print('      {}end else begin'.format(indent), file=dest)
        print('        {}counter <= 0;'.format(indent), file=dest)
        print('        {}flag <= ~flag;'.format(indent), file=dest)
        print('      {}end'.format(indent), file=dest)
        if has_condition(expr):
            print('      end', file=dest)
        print('    end', file=dest)
        print('  end', file=dest)
        
    if has_condition(expr):
        connections = [".CLOCK(CLOCK)", ".RESET(RESET)"]
        for c in children_info.get('outport', []):
            if(c[0]):
                connections.append(".{0}({0}_w)".format(c[1]))
        if has_condition(expr) and children_info.get('outport', [])[-1][0] == False:
            connections.append(".{0}({0}_w)".format(children_info.get('outport', [])[-1][1]))
        print('  bl_{0} {0}_inst('.format(gen_nested_module_name(name)), file=dest)
        print('    {}'.format(",".join(connections)), file=dest)
        print('  );', file=dest)
        
    print('endmodule // {}'.format(name), file=dest)
    
    l = children_info.get('outport', [])
    l.append([has_specified_output_port(expr), outport])
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
    print('    repeat(10000) @(posedge clk);', file=dest)
    print('    $finish;', file=dest)
    print('  end', file=dest)
    
    connections = [".CLOCK(clk)", ".RESET(reset)"]
    for c in info.get('outport', []):
        if(c[0]):
            print("  wire {}_w;".format(c[1]), file=dest)
            connections.append(".{0}({0}_w)".format(c[1]))
    if has_condition(expr) and info.get('outport', [])[-1][0] == False:
        print("  wire {}_w;".format(info.get('outport', [])[-1][1]), file=dest)
        connections.append(".{0}({0}_w)".format(info.get('outport', [])[-1][1]))
    print('  bl_{0} {0}_inst('.format(name), file=dest)
    print('    {}'.format(",".join(connections)), file=dest)
    print('  );', file=dest)

    print('endmodule', file=dest)


def generate_quartus_project(dest, expr, name):
    device = expr.get(":device", "5CEBA4F23C7")
    family = "Cyclone V"
    if(device.startswith("5C")):
        family = "Cyclone V"
        
    print("set_global_assignment -name FAMILY \"{}\"".format(family), file=dest)
    print("set_global_assignment -name DEVICE {}".format(device), file=dest)
    print("set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files", file=dest)
    print("set_global_assignment -name TOP_LEVEL_ENTITY bl_{}".format(name), file=dest)
    print('set_global_assignment -name VERILOG_FILE {}.v'.format(name), file=dest)
    for p in expr.get(":port", {}).items():
        if type(p[1]) is list:
            print("set_location_assignment PIN_{} -to {}".format(p[1][0].value(), p[0]), file=dest)
            print('set_instance_assignment -name IO_STANDARD "{}" -to {}'.format(p[1][1], p[0]), file=dest)
        else:
            print("set_location_assignment PIN_{} -to {}".format(p[1].value(), p[0]), file=dest)
    if ":period" in expr.keys():
        print("set_global_assignment -name SDC_FILE {}.sdc".format(name), file=dest)


def generate(name, expr):
    ss = io.StringIO()
    info = generate_counter_module(ss, expr, name)
    with open(name+".v", "w") as g:
        print(ss.getvalue(), file=g)
        
    ss = io.StringIO()
    generate_testbench_module(ss, expr, name, info)
    with open("tb_"+name+".v", "w") as g:
        print(ss.getvalue(), file=g)

    if not ':synth-tool' in expr.keys():
        return
        
    if(expr[':synth-tool'] == "QUARTUS"):
        ss = io.StringIO()
        generate_quartus_project(ss, expr, name)
        with open(name+".qsf", "w") as g:
            print(ss.getvalue(), file=g)
        with open(name+".qpf", "w") as g:
            print("PROJECT_REVISION = {}".format(name), file=g)
        with open(name+".sdc", "w") as g:
            print("set_time_format -unit ns -decimal_places 3", file=g)
            for p in expr.get(":period", {}).items():
                s = p[0]
                v = float(p[1])
                v0 = '{:.3f}'.format(v)
                v1 = '{:.3f}'.format(v/2)
                print("create_clock -name {"+s+"}", "-period {"+v0+"} -waveform {0.000 "+v1+"}", file=g)
