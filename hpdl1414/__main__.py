import argparse
from .hpdl1414 import HPDL1414, Top
from nmigen.cli import main_parser, main_runner
from nmigen_boards.chubbyhat_v0_1 import ChubbyHat_V01Platform
from nmigen.build import *

hpdl1414_pmod = [
    Resource("hpdl1414", 0,
             Subsignal("data", PinsN("1 2 3 4 7 8 9", dir="o", conn=("pmod", 4)), Attrs(IO_TYPE="LVCMOS33")),
             Subsignal("addr", PinsN("1 2", dir="o", conn=("pmod", 5)), Attrs(IO_TYPE="LVCMOS33")),
             Subsignal("n_wrs", PinsN("3 4 7 8 9", dir="o", conn=("pmod", 5)), Attrs(IO_TYPE="LVCMOS33"))
    )
]

def extra_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", type=int, default=2, help="number of displays")
    parser.add_argument("-t", "--text", type=str, default=" nmigen", help="text to display")
    return parser

if __name__ == "__main__":
    parser = main_parser(extra_options())
    args = parser.parse_args()

    plat = ChubbyHat_V01Platform()
    plat.add_resources(hpdl1414_pmod)
    top = Top(plat.default_clk_frequency, args.num, args.text)

    if args.action:
        main_runner(parser, args, top, ports=top.ports)
    else:
        plat.build(top, do_program=True)
