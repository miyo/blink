import io

from blink import generator
from blink import parser
from blink import data

def test_example_nest():
    name = 'nest'
    src = '''(L 1 :at (L 2 :at (L 4 :at (L 4))))'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_nest_c_c_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  reg [2-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 2'd0;
      flag <= 0;
    end else begin
      if(counter < 2'd3) begin
        counter <= counter + 2'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // nest_c_c_c
module bl_nest_c_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  wire Q_w;
  reg Q_d = 0;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q_d <= 0;
    end else begin
      Q_d <= Q_w;
    end
  end
  reg [2-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 2'd0;
      flag <= 0;
    end else begin
      if(Q_d != Q_w && Q_d == 0) begin
        if(counter < 2'd3) begin
          counter <= counter + 2'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest_c_c_c nest_c_c_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q(Q_w)
  );
endmodule // nest_c_c
module bl_nest_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  wire Q_w;
  reg Q_d = 0;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q_d <= 0;
    end else begin
      Q_d <= Q_w;
    end
  end
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(Q_d != Q_w && Q_d == 0) begin
        if(counter < 1'd1) begin
          counter <= counter + 1'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest_c_c nest_c_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q(Q_w)
  );
endmodule // nest_c
module bl_nest
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  wire Q_w;
  reg Q_d = 0;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q_d <= 0;
    end else begin
      Q_d <= Q_w;
    end
  end
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(Q_d != Q_w && Q_d == 0) begin
        if(counter < 1'd0) begin
          counter <= counter + 1'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest_c nest_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q(Q_w)
  );
endmodule // nest
'''
    
    assert(expected_verilog == ss.getvalue())

def test_example_nest2():
    name = 'nest2'
    src = '''(L 1 :at (L 2 :at (L 3 :at (L 4 :out Q0) :out Q1) :out Q2) :out Q3)'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_nest2_c_c_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0
);
  reg flag = 0;
  assign Q0 = flag;
  reg [2-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 2'd0;
      flag <= 0;
    end else begin
      if(counter < 2'd3) begin
        counter <= counter + 2'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // nest2_c_c_c
module bl_nest2_c_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0,
  output wire Q1
);
  reg flag = 0;
  assign Q1 = flag;
  wire Q0_w;
  reg Q0_d = 0;
  assign Q0 = Q0_d;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q0_d <= 0;
    end else begin
      Q0_d <= Q0_w;
    end
  end
  reg [2-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 2'd0;
      flag <= 0;
    end else begin
      if(Q0_d != Q0_w && Q0_d == 0) begin
        if(counter < 2'd2) begin
          counter <= counter + 2'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest2_c_c_c nest2_c_c_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q0(Q0_w)
  );
endmodule // nest2_c_c
module bl_nest2_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0,
  output wire Q1,
  output wire Q2
);
  reg flag = 0;
  assign Q2 = flag;
  wire Q0_w;
  reg Q0_d = 0;
  assign Q0 = Q0_d;
  wire Q1_w;
  reg Q1_d = 0;
  assign Q1 = Q1_d;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q0_d <= 0;
      Q1_d <= 0;
    end else begin
      Q0_d <= Q0_w;
      Q1_d <= Q1_w;
    end
  end
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(Q1_d != Q1_w && Q1_d == 0) begin
        if(counter < 1'd1) begin
          counter <= counter + 1'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest2_c_c nest2_c_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q0(Q0_w),.Q1(Q1_w)
  );
endmodule // nest2_c
module bl_nest2
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0,
  output wire Q1,
  output wire Q2,
  output wire Q3
);
  reg flag = 0;
  assign Q3 = flag;
  wire Q0_w;
  reg Q0_d = 0;
  assign Q0 = Q0_d;
  wire Q1_w;
  reg Q1_d = 0;
  assign Q1 = Q1_d;
  wire Q2_w;
  reg Q2_d = 0;
  assign Q2 = Q2_d;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q0_d <= 0;
      Q1_d <= 0;
      Q2_d <= 0;
    end else begin
      Q0_d <= Q0_w;
      Q1_d <= Q1_w;
      Q2_d <= Q2_w;
    end
  end
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(Q2_d != Q2_w && Q2_d == 0) begin
        if(counter < 1'd0) begin
          counter <= counter + 1'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest2_c nest2_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q0(Q0_w),.Q1(Q1_w),.Q2(Q2_w)
  );
endmodule // nest2
'''
    assert(expected_verilog == ss.getvalue())

def test_example_nest3():
    name = 'nest3'
    src = '''(L 1 :at (L 1 :at (L 10 :at (L 2500000 :out Q0) :out Q1) :out Q2) :out Q3
   :synth-tool "QUARTUS"
   :device "5CEBA4F23C7"
   :iomap '(CLOCK M9 RESET U13 Q3 Y3 Q2 W2 Q1 AA1 Q0 AA2)
   :period '(CLOCK 20.0)
   )
'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_nest3_c_c_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0
);
  reg flag = 0;
  assign Q0 = flag;
  reg [22-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 22'd0;
      flag <= 0;
    end else begin
      if(counter < 22'd2499999) begin
        counter <= counter + 22'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // nest3_c_c_c
module bl_nest3_c_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0,
  output wire Q1
);
  reg flag = 0;
  assign Q1 = flag;
  wire Q0_w;
  reg Q0_d = 0;
  assign Q0 = Q0_d;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q0_d <= 0;
    end else begin
      Q0_d <= Q0_w;
    end
  end
  reg [4-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 4'd0;
      flag <= 0;
    end else begin
      if(Q0_d != Q0_w && Q0_d == 0) begin
        if(counter < 4'd9) begin
          counter <= counter + 4'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest3_c_c_c nest3_c_c_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q0(Q0_w)
  );
endmodule // nest3_c_c
module bl_nest3_c
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0,
  output wire Q1,
  output wire Q2
);
  reg flag = 0;
  assign Q2 = flag;
  wire Q0_w;
  reg Q0_d = 0;
  assign Q0 = Q0_d;
  wire Q1_w;
  reg Q1_d = 0;
  assign Q1 = Q1_d;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q0_d <= 0;
      Q1_d <= 0;
    end else begin
      Q0_d <= Q0_w;
      Q1_d <= Q1_w;
    end
  end
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(Q1_d != Q1_w && Q1_d == 0) begin
        if(counter < 1'd0) begin
          counter <= counter + 1'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest3_c_c nest3_c_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q0(Q0_w),.Q1(Q1_w)
  );
endmodule // nest3_c
module bl_nest3
(
  input wire CLOCK,
  input wire RESET,
  output wire Q0,
  output wire Q1,
  output wire Q2,
  output wire Q3
);
  reg flag = 0;
  assign Q3 = flag;
  wire Q0_w;
  reg Q0_d = 0;
  assign Q0 = Q0_d;
  wire Q1_w;
  reg Q1_d = 0;
  assign Q1 = Q1_d;
  wire Q2_w;
  reg Q2_d = 0;
  assign Q2 = Q2_d;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q0_d <= 0;
      Q1_d <= 0;
      Q2_d <= 0;
    end else begin
      Q0_d <= Q0_w;
      Q1_d <= Q1_w;
      Q2_d <= Q2_w;
    end
  end
  reg [1-1:0] counter;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      counter <= 1'd0;
      flag <= 0;
    end else begin
      if(Q2_d != Q2_w && Q2_d == 0) begin
        if(counter < 1'd0) begin
          counter <= counter + 1'd1;
        end else begin
          counter <= 0;
          flag <= ~flag;
        end
      end
    end
  end
  bl_nest3_c nest3_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q0(Q0_w),.Q1(Q1_w),.Q2(Q2_w)
  );
endmodule // nest3
'''
    assert(expected_verilog == ss.getvalue())

    expected_testbench = '''module tb_nest3
(
);
  reg clk = 0;
  always begin
    #1 clk = ~clk;
  end
  reg reset;
  initial begin
    $dumpfile("nest3.vcd");
    $dumpvars(0);
    reset = 1;
    repeat(10) @(posedge clk);
    reset <= 0;
    repeat(10000) @(posedge clk);
    $finish;
  end
  wire Q0_w;
  wire Q1_w;
  wire Q2_w;
  wire Q3_w;
  bl_nest3 nest3_inst(
    .CLOCK(clk),.RESET(reset),.Q0(Q0_w),.Q1(Q1_w),.Q2(Q2_w),.Q3(Q3_w)
  );
endmodule
'''
    
    ss = io.StringIO()
    generator.generate_testbench_module(ss, expr, name, info)
    assert(expected_testbench == ss.getvalue())

    expected_qsf = '''set_global_assignment -name FAMILY "Cyclone V"
set_global_assignment -name DEVICE 5CEBA4F23C7
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name TOP_LEVEL_ENTITY bl_nest3
set_global_assignment -name VERILOG_FILE nest3.v
set_location_assignment PIN_M9 -to CLOCK
set_location_assignment PIN_U13 -to RESET
set_location_assignment PIN_Y3 -to Q3
set_location_assignment PIN_W2 -to Q2
set_location_assignment PIN_AA1 -to Q1
set_location_assignment PIN_AA2 -to Q0
set_global_assignment -name SDC_FILE nest3.sdc
'''

    ss = io.StringIO()
    generator.generate_quartus_qsf(ss, expr, name)
    assert(expected_qsf == ss.getvalue())

    expected_qpf = '''PROJECT_REVISION = nest3
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

def test_example_nest4():
    name = 'nest4'
    src = '''(L 0 :at (L 2))'''
    expr = parser.parse_source(src)
    ss = io.StringIO()
    info = generator.generate_counter_module(ss, expr, name)
    
    expected_verilog='''module bl_nest4_c
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
      if(counter < 1'd1) begin
        counter <= counter + 1'd1;
      end else begin
        counter <= 0;
        flag <= ~flag;
      end
    end
  end
endmodule // nest4_c
module bl_nest4
(
  input wire CLOCK,
  input wire RESET,
  output wire Q
);
  reg flag = 0;
  assign Q = flag;
  wire Q_w;
  reg Q_d = 0;
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      Q_d <= 0;
    end else begin
      Q_d <= Q_w;
    end
  end
  always @(posedge CLOCK) begin
    if(RESET == 1) begin
      flag <= 0;
    end else begin
      flag <= Q_w;
    end
  end
  bl_nest4_c nest4_c_inst(
    .CLOCK(CLOCK),.RESET(RESET),.Q(Q_w)
  );
endmodule // nest4
'''
    assert(expected_verilog == ss.getvalue())
