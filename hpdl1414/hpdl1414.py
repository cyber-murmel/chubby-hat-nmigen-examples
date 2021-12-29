from math import ceil
from nmigen import *

class Top(Elaboratable):
    def __init__(self, clk_frequency, num_displays=1, text=""):
        self.clk_frequency = clk_frequency
        self.num_displays = num_displays
        self.text = text.upper() + " "*(num_displays*4-len(text))
        self.hpdl1414 = HPDL1414(self.clk_frequency, self.num_displays)

    @property
    def ports(self):
        return self.hpdl1414.ports

    def elaborate(self, platform):
        m = Module()
        m.submodules.hpdl1414 = self.hpdl1414

        if platform:
            hpdl1414_pins = platform.request("hpdl1414", 0)
            # for some reason we have to negate all signals
            m.d.comb += hpdl1414_pins.data.eq(~self.hpdl1414.data)
            m.d.comb += hpdl1414_pins.addr.eq(~self.hpdl1414.addr)
            m.d.comb += hpdl1414_pins.n_wrs.eq(~self.hpdl1414.n_wrs)

        with m.FSM(reset="0") as fsm:
            for i in range(self.num_displays * HPDL1414.CHARS_PER_DISPLAY):

                state_name = "{}".format(i)
                next_state_name = "{}".format(i+1) if i+1 < (self.num_displays * HPDL1414.CHARS_PER_DISPLAY) else "STOP"

                with m.State(state_name):
                    m.d.sync += self.hpdl1414.char.eq(ord(self.text[i]))
                    m.d.sync += self.hpdl1414.pos.eq(i)
                    m.d.sync += self.hpdl1414.start.eq(1)
                    m.next = state_name+"_WAIT"

                with m.State(state_name+"_WAIT"):
                    m.d.sync += self.hpdl1414.start.eq(0)
                    with m.If(~(self.hpdl1414.busy | self.hpdl1414.start)):
                        m.next = next_state_name

            with m.State("STOP"):
                m.next = "STOP"

        return m

class HPDL1414(Elaboratable):
    # pdf.datasheetcatalog.com/datasheet/hp/HPDL-1414.pdf
    CHARS_PER_DISPLAY = 4
    DELAY_TIME =  20e-9
    SETUP_TIME =  130e-9
    HOLD_TIME =  50e-9

    def __init__(self, clk_frequency, num_displays=1):
        self.DELAY_TICKS = ceil(self.DELAY_TIME*clk_frequency)
        self.SETUP_TICKS = ceil(self.SETUP_TIME*clk_frequency)
        self.HOLD_TICKS = ceil(self.HOLD_TIME*clk_frequency)
        # incoming signal
        self.char = Signal(8)   # ASCII character
        self.pos = Signal(range(num_displays*4))  # position; left = 0
        self.start = Signal()   # start write
        # outgoing signal
        self.data = Signal(7)   # connect to D pins of displays
        self.addr = Signal(2)   # connect to A pins of displays
        self.n_wrs = Signal(num_displays, reset=-1)   # connect one to each n_wr pin of displays
        self.busy = Signal()    # indicate business

    @property
    def ports(self):
        return (self.pos, self.char, self.start, self.busy, self.n_wrs, self.addr, self.data)

    def elaborate(self, platform):
        m = Module()
        # counter for timing
        cnt = Signal(range(max(self.DELAY_TICKS, self.SETUP_TICKS, self.HOLD_TICKS)+1), reset=0)
        # "local variables"
        char = Signal(self.char.shape())
        pos = Signal(self.pos.shape())
        # address always is equal to 2 lsbs of position
        m.d.comb += self.addr.eq((self.CHARS_PER_DISPLAY-1) -pos[:2])

        with m.If(cnt > 0):
            m.d.sync += cnt.eq(cnt-1)

        with m.FSM(reset="IDLE") as fsm:
            with m.State("IDLE"):
                with m.If(self.start):
                    m.next = "DELAY"
                    m.d.sync += cnt.eq(self.DELAY_TICKS-1)

                    m.d.sync += char.eq(self.char)
                    m.d.sync += pos.eq(self.pos)

                    m.d.sync += self.busy.eq(1)

            with m.State("DELAY"):
                with m.If(cnt == 0):
                    m.next = "SETUP"
                    m.d.sync += cnt.eq(self.SETUP_TICKS-1)

                    m.d.sync += self.data.eq(char)
                    m.d.sync += self.n_wrs.eq(~(1<<pos[2:]))

            with m.State("SETUP"):
                with m.If(cnt == 0):
                    m.next = "HOLD"
                    m.d.sync += cnt.eq(self.HOLD_TICKS-1)

                    m.d.sync += self.n_wrs.eq(-1)

            with m.State("HOLD"):
                with m.If(cnt == 0):
                    m.next = "IDLE"
                    m.d.sync += cnt.eq(self.HOLD_TICKS-1)

                    m.d.sync += self.busy.eq(0)

        return m
