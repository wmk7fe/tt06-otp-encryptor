module tt_um_opt_encryptor (    
    input  [7:0] ui_in,    // Dedicated inputs
    output [7:0] uo_out,   // Dedicated outputs
    input  [7:0] uio_in,   // IOs: Input path
    output [7:0] uio_out,  // IOs: Output path
    output [7:0] uio_oe,
    input        ena,      // will go high when the design is enabled
    input        clk,      // clock
    input        rst_n     // reset_n - low to reset
        );

wire [7:0] data;
wire [7:0] pad_read;
wire [7:0] pad_gen;
wire [2:0] r_num;
reg[2:0] count = 4'd0;
wire decrypt;

reg [7:0] out;
reg [2:0] index_out;


// io
assign data = ui_in[7:0];
assign decrypt = uio_in[0];
assign r_num = uio_in[3:1];

assign uo_out[7:0] = out[7:0];
assign uio_out[6:4] = index_out[2:0];
assign uio_out[7] = 1'b0;

assign uio_out[3:0] = uio_in[7:4];

assign uio_oe = 8'b11110000;


register_file rf (
.reset(~rst_n),
.clock(clk),
.we(ena & ~decrypt),
.a1(r_num),
.wd(pad_gen),
.wa(count),
.rd1(pad_read));


LFSR_PRNG rng(
    .clk(clk),
    .rst(~rst_n),
    .prn(pad_gen));

//assign out = ena ? (decrypt ? (pad_read ^ data) : (pad_gen ^ data)) : 8'h00;
	 
always @ (posedge clk) begin
	if (~rst_n) begin
		count = 4'd0;
		out <= 8'h00;
	end
	else if (ena) begin
		if (decrypt) begin
			index_out = 3'h0;
			out <= pad_read ^ data;
		end
		else begin // encrypt
			if(count == 3'b111) begin
				index_out = count;
				count = 3'b000;
			end
			else begin
				index_out = count;
				count = count + 4'd1;
			end
			out <= pad_gen ^ data;
		end
	end
	else out <= 8'h00;
end
    
endmodule
