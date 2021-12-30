from nmigen import *
from nmigen.asserts import *

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
        self.counter = Signal(range(self.half_period + 1))

    @property
    def ports(self):
        return (self.blink_out, self.counter, )

    def elaborate(self, platform):
        m = Module()

        # Formal Verification
        if not platform:
            m.d.comb += [
                # assert counter stays in range
                Assert(self.counter <= self.half_period),
                # cover being on and off
                Cover(self.blink_out == 1),
                Cover(self.blink_out == 0),
            ]
            # ignore the first cycle
            with m.If(~Past(ResetSignal())):
                # counter reaches 0
                with m.If(Past(self.counter) == 0):
                    m.d.sync += [
                        # assert counter gets reset and LED flips
                        Assert(self.counter == self.half_period),
                        Assert(self.blink_out != Past(self.blink_out)),
                        # cover turning on and off
                        Cover(self.blink_out == 1),
                        Cover(self.blink_out == 0),
                    ]
                with m.Else():
                    m.d.comb += [
                        # assert that counter is counting and LED keeps state
                        Assert(self.counter == Past(self.counter)-1),
                        Assert(self.blink_out == Past(self.blink_out)),
                        # cover being on and off
                        Cover(self.blink_out == 1),
                        Cover(self.blink_out == 0),
                    ]
        # Behaviour
        with m.If(self.counter == 0):
            m.d.sync += [
                self.blink_out.eq(~self.blink_out),
                self.counter.eq(self.half_period)
            ]
        with m.Else():
            m.d.sync += self.counter.eq(self.counter - 1)

        return m
