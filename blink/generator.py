import math


def generate_counter_module(dest, expr, name):
    bitwidth = math.floor(math.log2(expr['value'])) + 1

    print('module {}'.format(name), file=dest)
    print('(', file=dest)
    print('  input wire clk,', file=dest)
    print('  input wire reset,', file=dest)
    print('  output wire q', file=dest)
    print(');', file=dest)
    print('  reg [{}-1:0] counter;'.format(bitwidth), file=dest)
    print('  reg flag;', file=dest)
    print('  assign q = flag;', file=dest)
    print('  always @(posedge clk) begin', file=dest)
    print('    if(reset == 1) begin', file=dest)
    print("      counter <= {}'d0;".format(bitwidth), file=dest)
    print('      flag <= 0;', file=dest)
    print('    end else begin', file=dest)
    print("      if(counter < {}'d{}) begin".format(bitwidth, expr['value']), file=dest)
    print("        counter <= counter + {}'d1;".format(bitwidth), file=dest)
    print('      end else begin', file=dest)
    print('        counter <= 0;', file=dest)
    print('        flag <= ~flag;', file=dest)
    print('      end', file=dest)
    print('    end', file=dest)
    print('  end', file=dest)
    print('endmodule', file=dest)


def generate_testbench_module(dest, expr, name):
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
    
    print('  {0} {0}_inst'.format(name), file=dest)
    print('    (', file=dest)
    print('      .clk(clk),', file=dest)
    print('      .reset(reset),', file=dest)
    print('      .q(q)', file=dest)
    print('    );', file=dest)

    print('endmodule', file=dest)
