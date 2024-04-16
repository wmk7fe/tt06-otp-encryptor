# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

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
  
  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 0
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await ClockCycles(dut.clk, 10)
  dut.rst_n.value = 1

  # Set the input values, wait one clock cycle, and check the output
  dut._log.info("Test Encryption")
  dut.ena.value = 1
  dut.ui_in.value = 0xab
  dut.uio_in.value = 0b00000000

  await ClockCycles(dut.clk, 1)

  dut._log.info(f'Encrypted output: {data_out.value} ({rnum_out.value >> 4})')
  data = data_out.value
  rnum = rnum_out.value >> 4

  await ClockCycles(dut.clk, 3)

  dut._log.info("Test Decryption")
  dut.ena.value = 1
  dut.ui_in.value = data
  dut.uio_in.value = 0b00000001

  await ClockCycles(dut.clk, 1)

  dut._log.info(f'Encrypted output: {data_out.value} ({rnum_out.value >> 4})')
  data = data_out.value

  

  
