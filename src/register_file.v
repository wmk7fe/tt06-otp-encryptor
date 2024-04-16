module register_file(reset,clock,we,a1,wd,wa,rd1);
   
   input reset;
   input clock;
   input we; // write-enable
   input [2:0] a1; // register address 1
   input [7:0] wd; // write data
   input [2:0] wa; // write address
   output reg [7:0] rd1; // read register 1
	
	reg[7:0] mem[0:7];
	
	integer i;
	always @ (posedge clock, posedge reset) begin
		if (reset) begin
			for(i = 0; i < 8; i = i + 1) begin
				mem[i] <= 8'h00;
			end
		end
		else if (we) begin
			mem[wa] <= wd;
			rd1 = 8'h00;
		end
		else begin
			rd1 = mem[a1];
		end
	end

endmodule
