from nmigen import *

class Top(Elaboratable):
    def __init__(self, clk_frequency, period_s):
        period = clk_frequency * period_s
        self.blinker = Blinker(period)

    @property
    def ports(self):
        return self.blinker.ports

    def elaborate(self, platform):
        m = Module()

        m.submodules.blinker = self.blinker

        if(platform):
            ledg_n = platform.request("led")
            m.d.comb += [
                ledg_n.eq(self.blinker.blink_out)
            ]

        return m

class Blinker(Elaboratable):
    def __init__(self, period=2):
        self.half_period = int(period / 2) - 1 # one extra cycle is need for reloading the value
        self.blink_out = Signal(1)

    @property
    def ports(self):
        return (self.blink_out, )

    def elaborate(self, _platform):
        m = Module()

        self.counter = Signal(range(self.half_period + 1))

        with m.If(self.counter == 0):
            m.d.sync += [
                self.blink_out.eq(~self.blink_out),
                self.counter.eq(self.half_period)
            ]
        with m.Else():
            m.d.sync += self.counter.eq(self.counter - 1)

        return m
