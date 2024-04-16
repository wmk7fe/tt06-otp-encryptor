module LFSR_PRNG (
    clk,
    rst,
    prn);

    input clk;
    input rst;
    output [7:0] prn;

    reg [31:0] D32 = 32'hbdca2c92; //NEVER 000000

    assign prn[0] = D32[23];
    assign prn[1] = D32[17];
    assign prn[2] = D32[13];
	 assign prn[3] = D32[11];
	 assign prn[4] = D32[7];
	 assign prn[5] = D32[5];
	 assign prn[6] = D32[3];
	 assign prn[7] = D32[2];

    always @ (posedge rst or posedge clk)
    if (rst)
        begin
            D32 <= 32'hbdca2c92;
        end
    else
        begin
            D32[1] <= D32[0];
            D32[2] <= D32[1];
            D32[3] <= D32[2];
            D32[4] <= D32[3];
            D32[5] <= D32[4];
				D32[6] <= D32[5];
				D32[7] <= D32[6];
				D32[8] <= D32[7];
				D32[9] <= D32[8];
				D32[10] <= D32[9];
				D32[11] <= D32[10];
				D32[12] <= D32[11];
				D32[13] <= D32[12];
				D32[14] <= D32[13];
				D32[15] <= D32[14];
            D32[16] <= D32[15];
				D32[17] <= D32[16];
            D32[18] <= D32[17];
            D32[19] <= D32[18];
            D32[20] <= D32[19];
            D32[21] <= D32[20];
				D32[22] <= D32[21];
				D32[23] <= D32[22];
				D32[24] <= D32[23];
				D32[25] <= D32[24];
				D32[26] <= D32[25];
				D32[27] <= D32[26];
				D32[28] <= D32[27];
				D32[29] <= D32[28];
				D32[30] <= D32[29];
				D32[31] <= D32[30];
				D32[0] <= ~(~(~(D32[31] ^ D32[21]) ^ D32[1]) ^ D32[0]);
        end
		  
endmodule
