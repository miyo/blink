import io

from blink import generator
from blink import parser
from blink import data

def test_example_test0():
    name = 'test0'
    src = '''(L 0)'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_test0
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
endmodule // test0
'''
    
    assert(expected_verilog == ss.getvalue())

def test_example_test1():
    name = 'test1'
    src = '''(L 1)'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_test1
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(counter < 1'd0) begin
        counter <= counter + 1'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // test1
'''
    assert(expected_verilog == ss.getvalue())

def test_example_test8():
    name = 'test8'
    src = '''(L 8)'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_test8
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  reg [3-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 3'd0;
      flag <= 0;
    end else begin
      if(counter < 3'd7) begin
        counter <= counter + 3'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // test8
'''
    assert(expected_verilog == ss.getvalue())

def test_example_test9():
    name = 'test9'
    src = '''(L 9)'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_test9
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  reg [4-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 4'd0;
      flag <= 0;
    end else begin
      if(counter < 4'd8) begin
        counter <= counter + 4'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // test9
'''
    assert(expected_verilog == ss.getvalue())

