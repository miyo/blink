import io

from blink import generator
from blink import data

def test_generator_L():
    expr = data.Counter(64)
    name = "blink"
    ss = io.StringIO()
    generator.generate_counter_module(ss, expr, name)

    expected = '''module bl_blink
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  reg [6-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 6'd0;
      flag <= 0;
    end else begin
      if(counter < 6'd63) begin
        counter <= counter + 6'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // blink
'''
    assert(expected == ss.getvalue())

def test_gen_bitwidth():
    assert(generator.gen_bitwidth(0) == 1)
    assert(generator.gen_bitwidth(1) == 1)
    assert(generator.gen_bitwidth(2) == 2)
    assert(generator.gen_bitwidth(3) == 2)
    assert(generator.gen_bitwidth(4) == 3)
    assert(generator.gen_bitwidth(5) == 3)
    assert(generator.gen_bitwidth(6) == 3)
    assert(generator.gen_bitwidth(7) == 3)
    assert(generator.gen_bitwidth(8) == 4)
    assert(generator.gen_bitwidth(15) == 4)
    assert(generator.gen_bitwidth(16) == 5)
    assert(generator.gen_bitwidth(31) == 5)
    assert(generator.gen_bitwidth(32) == 6)
    assert(generator.gen_bitwidth(63) == 6)
    assert(generator.gen_bitwidth(64) == 7)
    assert(generator.gen_bitwidth(127) == 7)
    assert(generator.gen_bitwidth(128) == 8)
