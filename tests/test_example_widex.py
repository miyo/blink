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

def test_example_wide2():
    name = 'wide2'
    src = '''(L 4294967296 :out '(Q 29 20)
   :synth-tool "QUARTUS"
   :device "5CEBA4F23C7"
   :iomap '(CLOCK (M9 "3.3-V LVTTL") RESET (U13 "3.3-V LVTTL")
	    Q ((AA2 "3.3-V LVTTL")
	       (AA1 "3.3-V LVTTL")
	       (W2 "3.3-V LVTTL")
	       (Y3 "3.3-V LVTTL")
	       (N2 "3.3-V LVTTL")
	       (N1 "3.3-V LVTTL")
	       (U2 "3.3-V LVTTL")
	       (U1 "3.3-V LVTTL")
	       (L2 "3.3-V LVTTL")
	       (L1 "3.3-V LVTTL")))
   :period '(CLOCK 20.0)
   )'''

    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_wide2
(
  input wire CLOCK,
  input wire RESET,
  output wire [10-1:0] Q
);
  reg [32-1:0] counter;
  assign Q = counter[29:20];
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 32'd0;
    end else begin
      if(counter < 32'd4294967295) begin
        counter <= counter + 32'd1;
      end else begin
        counter <= 0;
      end
    end
  end
endmodule // wide2
'''

    assert(expected_verilog == ss.getvalue())

    expected_testbench = '''module tb_wide2
(
);
  reg clk = 0;
  always begin
    #1 clk = ~clk;
  end
  reg reset;
  initial begin
    $dumpfile("wide2.vcd");
    $dumpvars(0);
    reset = 1;
    repeat(10) @(posedge clk);
    reset <= 0;
    repeat(10000) @(posedge clk);
    $finish;
  end
  wire [10-1:0] Q_w;
  bl_wide2 wide2_inst(
    .CLOCK(clk),.RESET(reset),.Q(Q_w)
  );
endmodule
'''
    ss = io.StringIO()
    generator.generate_testbench_module(ss, expr, name, info)
    assert(expected_testbench == ss.getvalue())

    expected_qsf = '''set_global_assignment -name FAMILY "Cyclone V"
set_global_assignment -name DEVICE 5CEBA4F23C7
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name TOP_LEVEL_ENTITY bl_wide2
set_global_assignment -name VERILOG_FILE wide2.v
set_location_assignment PIN_M9 -to CLOCK
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to CLOCK
set_location_assignment PIN_U13 -to RESET
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to RESET
set_location_assignment PIN_AA2 -to Q[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[0]
set_location_assignment PIN_AA1 -to Q[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[1]
set_location_assignment PIN_W2 -to Q[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[2]
set_location_assignment PIN_Y3 -to Q[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[3]
set_location_assignment PIN_N2 -to Q[4]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[4]
set_location_assignment PIN_N1 -to Q[5]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[5]
set_location_assignment PIN_U2 -to Q[6]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[6]
set_location_assignment PIN_U1 -to Q[7]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[7]
set_location_assignment PIN_L2 -to Q[8]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[8]
set_location_assignment PIN_L1 -to Q[9]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to Q[9]
set_global_assignment -name SDC_FILE wide2.sdc
'''

    ss = io.StringIO()
    generator.generate_quartus_qsf(ss, expr, name)
    assert(expected_qsf == ss.getvalue())

    expected_qpf = '''PROJECT_REVISION = wide2
'''

    ss = io.StringIO()
    generator.generate_quartus_qpf(ss, name)
    assert(expected_qpf == ss.getvalue())

    expected_sdc = '''set_time_format -unit ns -decimal_places 3
create_clock -name clk_CLOCK -period {20.000} -waveform {0.000 10.000} [get_ports {CLOCK}]
'''
    ss = io.StringIO()
    generator.generate_quartus_sdc(ss, expr)
    assert(expected_sdc == ss.getvalue())
