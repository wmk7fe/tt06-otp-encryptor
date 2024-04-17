![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# Tiny Tapeout Verilog Project Template

This is the one time pad encryptor submission for the Tiny Tapeout 06 Shuttle. The top level file is in src/tt_um_otp_encryptor.v, which includes a module from the file LFSR_PRNG.v in the design. Testing of this design is performed from the file test/test.py with encryptions and decryptions of different values as well as encryptions and decryptions of pads stored in different registers. More information on how the logic works and how to test is shown below.

## How it works

- 8 bit data inputs come through ui_in in the form of either plaintext or ciphertext. Bit 0 of uio_in is used to determine whether the chip will perform encryption or decryption. When it is high, decryption will be performed. When it is low, decryption will be performed. However, the enable signal must be high in both cases for either encryption or decryption to be performed. In the case of encryption, the chip will take an 8 bit value from an internal pseudorandom number generator to use as a one time pad. To create the ciphertext, the chip will xor the bits of the one time pad with their relative bits in the plaintext to create ciphertext. In order to later recover the plaintext, the one time pad is stored in an internal register file, and the index of the register of which the pad is stored in is outputed to bits 6 through 4 of uio_out. There are 8 registers in the register file (0-7). To decrypt ciphertext, the decrypt signal must be high (bit 0 of uio_in) and the index that the associated one time pad is stored in must be inputted to uio_in bits 3 through 1. Then, the one time pad will be recovered from the indexed register, the pad will be xored with the ciphertext, and the plaintext will be produced as output.

## How to test

- Testing can be performed by ensuring that inputted plaintext can be recovered by taking the encrypted output and register index and feeding it into the system.

## External hardware

- External hardware with basic memory, wiring, and data displaying functionality should be suitable to test this chip. Verilog testing was performed by using one external register for data output, one external register for index output, and a means to read the data from the registers. Basic binary instrumentation may be needed if direct access to wires is not possible in order to shift the register index from the output bits of 6 through 4 to the input bits of 3 through 1.
