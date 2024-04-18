
`default_nettype none

module tt_um_otp_encryptor (    
    input  [7:0] ui_in,    // Dedicated inputs
    output [7:0] uo_out,   // Dedicated outputs
/* verilator lint_off UNUSEDSIGNAL */
    input  [7:0] uio_in,   // IOs: Input path
/* verilator lint_on UNUSEDSIGNAL */
    output [7:0] uio_out,  // IOs: Output path
    output [7:0] uio_oe,
    input        ena,      // will go high when the design is enabled
    input        clk,      // clock
    input        rst_n     // reset_n - low to reset
        );

wire [7:0] data;
wire [7:0] pad_gen;
wire [2:0] r_num;
reg[2:0] count;
wire decrypt;
wire reset;

reg [7:0] out;
reg [2:0] index_out;


// io
assign data = ui_in[7:0];
assign decrypt = uio_in[0];
assign r_num = uio_in[3:1];
assign reset = ~rst_n;

assign uo_out[7:0] = out[7:0];
assign uio_out[6:4] = index_out[2:0];
	
assign uio_out[7] = 1'b0;
assign uio_out[3:0] = 4'h0;
assign uio_oe = 8'b11110000;

// registers	
reg[7:0] mem[0:7];
integer i;

LFSR_PRNG rng(
    .clk(clk),
    .rst(reset),
    .prn(pad_gen));

//assign out = ena ? (decrypt ? (pad_read ^ data) : (pad_gen ^ data)) : 8'h00;
	 
always @ (posedge clk, posedge reset) begin
	if (reset) begin
		count <= 3'h0;
		out <= 8'h00;
		index_out <= 3'h0;
		
		for(i = 0; i < 8; i = i + 1) begin
			mem[i] <= 8'h00;
		end
		
	end
	else if (ena) begin
		if (decrypt) begin
			index_out <= 3'h0;
			out <= mem[r_num] ^ data;
		end
		else begin // encrypt
			if(count == 3'b111) begin
				count <= 3'b000;
			end
			else begin
				count <= count + 3'h1;
			end
			out <= pad_gen ^ data;
			mem[count] <= pad_gen;
			index_out <= count;
		end
	end
	else out <= 8'h00;
end
    
endmodule
