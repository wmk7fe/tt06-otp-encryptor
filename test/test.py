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
    await print_io(dut)

    # Encrypt
    dut._log.info("Encrypt 0xab")
    await clock_rise(clk)
    await clock_fall(clk)

    ena.value = 1
    data_in.value = 0xab
    rnum_decrypt_in.value = 0x00

    await clock_rise(clk)
    await print_io(dut)
    await clock_fall(clk)
    await print_io(dut)
    await clock_rise(clk)
    await print_io(dut)
    await clock_fall(clk)
    await print_io(dut)
    await clock_rise(clk)
    await print_io(dut)
    await clock_fall(clk)
    await print_io(dut)

  

  
