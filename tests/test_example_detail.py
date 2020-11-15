import io

from blink import generator
from blink import parser
from blink import data

def test_example_detail():
    name = 'detail'
    
    src = '''(L 50000000
   :synth-tool "QUARTUS"
   :device "5CEBA4F23C7"
   :iomap '(CLOCK (M9 "3.3-V LVTTL") RESET (U13 "3.3-V LVTTL") Q (AA2 "3.3-V LVTTL"))
   :period '(CLOCK 20.0)
   )'''
    
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)

    expected_verilog='''module bl_detail
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  reg [26-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 26'd0;
      flag <= 0;
    end else begin
      if(counter < 26'd49999999) begin
        counter <= counter + 26'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // detail
'''

    assert(expected_verilog == ss.getvalue())

    expected_testbench = '''module tb_detail
(
);
  reg clk = 0;
  always begin
    #1 clk = ~clk;
  end
  reg reset;
  initial begin
    $dumpfile("detail.vcd");
    $dumpvars(0);
    reset = 1;
    repeat(10) @(posedge clk);
    reset <= 0;
    repeat(10000) @(posedge clk);
    $finish;
  end
  bl_detail detail_inst(
    .CLOCK(clk),.RESET(reset)
  );
endmodule
'''
    
    ss = io.StringIO()
    generator.generate_testbench_module(ss, expr, name, info)
    assert(expected_testbench == ss.getvalue())

    expected_qsf = '''set_global_assignment -name FAMILY "Cyclone V"
set_global_assignment -name DEVICE 5CEBA4F23C7
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name TOP_LEVEL_ENTITY bl_detail
set_global_assignment -name VERILOG_FILE detail.v
set_location_assignment PIN_M9 -to CLOCK
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to CLOCK
set_location_assignment PIN_U13 -to RESET
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to RESET
set_location_assignment PIN_AA2 -to Q
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q
set_global_assignment -name SDC_FILE detail.sdc
'''

    ss = io.StringIO()
    generator.generate_quartus_qsf(ss, expr, name)
    assert(expected_qsf == ss.getvalue())

    expected_qpf = '''PROJECT_REVISION = detail
'''

    ss = io.StringIO()
    generator.generate_quartus_qpf(ss, name)
    assert(expected_qpf == ss.getvalue())

    expected_sdc = '''set_time_format -unit ns -decimal_places 3
create_clock -name {CLOCK} -period {20.000} -waveform {0.000 10.000}
'''
    ss = io.StringIO()
    generator.generate_quartus_sdc(ss, expr)
    assert(expected_sdc == ss.getvalue())
