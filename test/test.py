# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

async def uio_in(rnum, decrypt):
    return 0xF & ((rnum << 1) + decrypt)

async def rnum(uio_out):
    return 0x7 & (uio_out >> 4)

async def clock_rise(clk):
    clk.value = 1
    await Timer(10, units='ns')

async def clock_fall(clk):
    clk.value = 0
    await Timer(10, units='ns')

async def print_io(dut):
    clk = dut.clk
    ena = dut.ena
    data_in = dut.ui_in
    data_out = dut.uo_out
    rnum_decrypt_in = dut.uio_in
    rnum_out = dut.uio_out
    rst_n = dut.rst_n
    dut._log.info(f'\n\tclk: {clk.value}\n\tena: {ena.value}\n\tdecrypt: {dut.uio_in.value & 0x1}\n\trnum: {(dut.uio_in.value>>1)&0x7}\n\tin: {data_in.value}\n\tout: {data_out.value}\n\trnum_out: {(dut.uio_out.value >> 4) & 0x7}\n')

# async def print_io_safe(dut):
#     clk = dut.clk
#     ena = dut.ena
#     data_in = dut.ui_in
#     data_out = dut.uo_out
#     rnum_decrypt_in = dut.uio_in
#     rnum_out = dut.uio_out
#     rst_n = dut.rst_n
#     dut._log.info(f'\n\tclk: {clk.value}\n\tena: {ena.value}\n\tdecrypt: {dut.uio_in.value & 0x1}\n\trnum: {(dut.uio_in.value>>1)&0x7}\n\tout: {data_out.value}\n\truio_out: {dut.uio_out.value}\n')

@cocotb.test()
async def test_project(dut):
    clk = dut.clk
    ena = dut.ena
    data_in = dut.ui_in
    data_out = dut.uo_out
    rnum_decrypt_in = dut.uio_in
    rnum_out = dut.uio_out
    rst_n = dut.rst_n
    
  
    dut._log.info("Start")
    # Reset
    dut._log.info("Reset")
    await clock_rise(clk)
    await clock_fall(clk)
    await clock_rise(clk)
    ena.value = 0
    rst_n.value = 1
    data_in.value = 0
    rnum_decrypt_in.value = 0
    await clock_rise(clk)
    await clock_fall(clk)
    rst_n.value = 0
    await clock_rise(clk)
    await clock_fall(clk)
    rst_n.value = 1
    ena.value = 1
    dut._log.info(f'out: {data_out.value}\n\tuio_out: {dut.uio_out.value}\n')

    # Encrypt
    dut._log.info("Encrypt 0xab - store to three different registers")
    await clock_rise(clk)
    await clock_fall(clk)

    data_in.value = 0xab
    rnum_decrypt_in.value = 0x00

    await clock_rise(clk)
    await clock_fall(clk)
    await print_io(dut)
    ct0 = data_out.value
    r0 = (dut.uio_out.value >> 4) & 0x7
    assert ct0 != 0xab, f"Encryption failed: Plaintext Unmodified"

    await clock_rise(clk)
    # await print_io(dut)
    await clock_fall(clk)
    await print_io(dut)
    ct1 = data_out.value
    r1 = (dut.uio_out.value >> 4) & 0x7
    assert ct1 != 0xab, f"Encryption failed: Plaintext Unmodified"
    
    await clock_rise(clk)
    # await print_io(dut)
    await clock_fall(clk)
    await print_io(dut)
    ct2 = data_out.value
    r2 = (dut.uio_out.value >> 4) & 0x7
    assert ct2 != 0xab, f"Encryption failed: Plaintext Unmodified"

    dut._log.info("Decrypt stored ciphertexts associated with r0, r1, r2")

    dut._log.info("r0")
    data_in.value = ct0
    rnum_decrypt_in.value = (r0 << 1) + 1
    await clock_rise(clk)
    await clock_fall(clk)
    await print_io(dut)
    assert data_out.value == 0xab
    assert data_out.value == 0xab, f"Decryption failed: expected 0xab, got {data_out.value} (r0)"

    dut._log.info("r1")
    data_in.value = ct1
    rnum_decrypt_in.value = (r1 << 1) + 1
    await clock_rise(clk)
    await clock_fall(clk)
    await print_io(dut)
    assert data_out.value == 0xab
    assert data_out.value == 0xab, f"Decryption failed: expected 0xab, got {data_out.value} (r1)"

    dut._log.info("r2")
    data_in.value = ct2
    rnum_decrypt_in.value = (r2 << 1) + 1
    await clock_rise(clk)
    await clock_fall(clk)
    await print_io(dut)
    assert data_out.value == 0xab, f"Decryption failed: expected 0xab, got {data_out.value} (r2)"

