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
    await Timer(20, units='us')

async def clock_fall(clk):
    clk.value = 0
    await Timer(20, units='us')

async def wait_x_cycles(clk, x):
    for i in range(x):
        await clock_rise(clk)
        await clock_fall(clk)

async def print_io(dut):
    clk = dut.clk
    ena = dut.ena
    data_in = dut.ui_in
    data_out = dut.uo_out
    rnum_decrypt_in = dut.uio_in
    rnum_out = dut.uio_out
    rst_n = dut.rst_n
    dut._log.info(f'\n\tclk: {clk.value}\n\tena: {ena.value}\n\tdecrypt: {dut.uio_in.value & 0x1}\n\trnum: {(dut.uio_in.value>>1)&0x7}\n\tin: {data_in.value}\n\tout: {data_out.value}\n\trnum_out: {(dut.uio_out.value >> 4) & 0x7}\n')

@cocotb.test()
async def test_otp_encryptor_vary_registers(dut):
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
    await clock_rise(clk)
    await clock_fall(clk)
    dut._log.info(f'out: {data_out.value}\n\tuio_out: {dut.uio_out.value}\n')

    # Encrypt
    dut._log.info("Encrypt 0xab - store to three different registers")
    await wait_x_cycles(clk, 3)

    data_in.value = 0xab
    rnum_decrypt_in.value = 0x00

    dut._log.info("\t1st Register")
    await wait_x_cycles(clk, 3)
    await print_io(dut)
    ct0 = data_out.value
    r0 = (dut.uio_out.value >> 4) & 0x7

    dut._log.info("\t2nd Register")
    await wait_x_cycles(clk, 3)
    await print_io(dut)
    ct1 = data_out.value
    r1 = (dut.uio_out.value >> 4) & 0x7

    dut._log.info("\t3rd Register")
    await wait_x_cycles(clk, 3)
    await print_io(dut)
    ct2 = data_out.value
    r2 = (dut.uio_out.value >> 4) & 0x7

    dut._log.info("Decrypt stored ciphertexts associated with each register")

    dut._log.info("\t1st Register")
    data_in.value = ct0
    rnum_decrypt_in.value = (r0 << 1) + 1
    await wait_x_cycles(clk, 5)
    await print_io(dut)
    assert data_out.value == 0xab, f"Decryption failed: expected 0xab, got {data_out.value} (r{r0})"

    dut._log.info("\t2nd Register")
    data_in.value = ct1
    rnum_decrypt_in.value = (r1 << 1) + 1
    await wait_x_cycles(clk, 5)
    await print_io(dut)
    assert data_out.value == 0xab, f"Decryption failed: expected 0xab, got {data_out.value} (r{r1})"

    dut._log.info("\t3rd Register")
    data_in.value = ct2
    rnum_decrypt_in.value = (r2 << 1) + 1
    await wait_x_cycles(clk, 5)
    await print_io(dut)
    assert data_out.value == 0xab, f"Decryption failed: expected 0xab, got {data_out.value} (r{r2})"


@cocotb.test()
async def test_otp_encryptor_large_num_set(dut):
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

    await clock_rise(clk)
    await clock_fall(clk)
    await clock_rise(clk)
    await clock_fall(clk)

    # Encrypt
    dut._log.info("Encrypt numbers 50 to 119")

    for i in range(80):
    
        data_in.value = i + 50
        rnum_decrypt_in.value = 0x00
    
        await wait_x_cycles(clk, 3)
        await print_io(dut)
        ct = data_out.value
        r = (dut.uio_out.value >> 4) & 0x7
    
        data_in.value = ct
        rnum_decrypt_in.value = (r << 1) + 1
        await wait_x_cycles(clk, 5)
        await print_io(dut)
        assert data_out.value == i + 50, f"Decryption failed: expected {i + 50}, got {data_out.value} (r{r}))"
    

