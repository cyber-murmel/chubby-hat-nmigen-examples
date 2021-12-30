import argparse
from .blink import Blinker, Top
from nmigen import *
from nmigen.asserts import *
from nmigen.cli import main_parser, main_runner
from nmigen_boards.chubbyhat_v0_1 import ChubbyHat_V01Platform

def extra_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--blink-freq", type=float, default=1, help="blink frequency")
    return parser

def prepare_formal_verification():
    period = 10
    m = Module()
    m.submodules.blinker = blinker = Blinker(period)

    m.d.comb += [
        # assert counter stays in range
        Assert(blinker.counter <= blinker.half_period),
        # cover being on and off
        Cover(blinker.blink_out == 1),
        Cover(blinker.blink_out == 0),
    ]
    # when the counter has reset
    with m.If(blinker.counter == blinker.half_period):
        m.d.comb += [
            # assert that the LED has fliped
            Assert(blinker.blink_out != Past(blinker.blink_out)),
            # cover turning on and off
            Cover(blinker.blink_out == 1),
            Cover(blinker.blink_out == 0),
        ]

    return m

if __name__ == "__main__":
    parser = main_parser(extra_options())
    args = parser.parse_args()

    if args.action:
        # if "simulate" == args.action:
        #     main_runner(parser, args, top, ports=top.ports)
        if "generate" == args.action:
            period = 10
            # module = prepare_formal_verification()
            m = Module()
            m.submodules.blinker = blinker = Blinker(period)
            main_runner(parser, args, m, ports=(ClockSignal(), ) + blinker.ports)
    else:
        plat = ChubbyHat_V01Platform()
        top = Top(plat.default_clk_frequency, 1/args.blink_freq)
        plat.build(top, do_program=True)
