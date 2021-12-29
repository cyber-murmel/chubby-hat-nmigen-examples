#!/usr/bin/env python3

from nmigen import *

class Top(Elaboratable):
    def __init__(self, maxperiod):
        self.blinker = Blinker(maxperiod)

    def elaborate(self, platform):
        ledg_n = platform.request("led")

        m = Module()

        m.submodules.blinker = self.blinker

        m.d.comb += [
            ledg_n.eq(self.blinker.blink_out)
        ]

        return m

class Blinker(Elaboratable):
    def __init__(self, maxperiod):
        self.maxperiod = maxperiod
        self.blink_out = Signal(1)
        self.counter = Signal(range(self.maxperiod + 1))

    def elaborate(self, _platform):
        m = Module()

        with m.If(self.counter == 0):
            m.d.sync += [
                self.blink_out.eq(~self.blink_out),
                self.counter.eq(self.maxperiod)
            ]
        with m.Else():
            m.d.sync += self.counter.eq(self.counter - 1)

        return m
