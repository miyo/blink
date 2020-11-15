import io

from blink import generator
from blink import parser
from blink import data

def test_example_wide():
    name = 'wide'
    src = '''(L 1024 :out '(Q 7 3))'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_wide
(
  input wire CLOCK,
  input wire RESET,
  output wire [5-1:0] Q
);
  reg [10-1:0] counter;
  assign Q = counter[7:3];
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 10'd0;
    end else begin
      if(counter < 10'd1023) begin
        counter <= counter + 10'd1;
      end else begin
        counter <= 0;
      end
    end
  end
endmodule // wide
'''

    assert(expected_verilog == ss.getvalue())

    expected_testbench = '''module tb_wide
(
);
  reg clk = 0;
  always begin
    #1 clk = ~clk;
  end
  reg reset;
  initial begin
    $dumpfile("wide.vcd");
    $dumpvars(0);
    reset = 1;
    repeat(10) @(posedge clk);
    reset <= 0;
    repeat(10000) @(posedge clk);
    $finish;
  end
  wire [5-1:0] Q_w;
  bl_wide wide_inst(
    .CLOCK(clk),.RESET(reset),.Q(Q_w)
  );
endmodule
'''
    
    ss = io.StringIO()
    generator.generate_testbench_module(ss, expr, name, info)
    assert(expected_testbench == ss.getvalue())
