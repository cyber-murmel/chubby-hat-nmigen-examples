import argparse
from .blink import Blinker, Top
from nmigen import *
from nmigen.asserts import *
from nmigen.cli import main_parser, main_runner
from nmigen_boards.chubbyhat_v0_1 import ChubbyHat_V01Platform


def extra_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--blink-freq", type=float, default=1, help="blink frequency"
    )
    return parser


if __name__ == "__main__":
    parser = main_parser(extra_options())
    args = parser.parse_args()

    plat = ChubbyHat_V01Platform()
    top = Top(plat.default_clk_frequency, 1 / args.blink_freq)

    if args.action:
        main_runner(parser, args, top, ports=top.ports)
    else:
        plat.build(top, do_program=True)
