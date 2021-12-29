import argparse
from .gamma_pdm import PDMDriver, Top
from nmigen.cli import main_parser, main_runner
from nmigen_boards.chubbyhat_v0_1 import ChubbyHat_V01Platform


def extra_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", type=float, default=2.2, help="Gamma exponent (default 2.2)")
    return parser

if __name__ == "__main__":
    parser = main_parser(extra_options())
    args = parser.parse_args()

    plat = ChubbyHat_V01Platform()
    top = Top(gamma=args.g)

    if args.action:
        main_runner(parser, args, top, ports=top.ports)
    else:
        plat.build(top, do_program=True)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-s", action="store_true", help="Simulate PDMDriver (for debugging).")
#     parser.add_argument("-g", type=float, default=2.2, help="Gamma exponent (default 2.2)")
#     args = parser.parse_args()

#     if args.s:
#         p = PDMDriver(8)
#         sim = Simulator(p)
#         sim.add_clock(1.0 / 12e6)

#         def out_proc():
#             for i in range(256):
#                 yield p.pdm_in.eq(i)
#                 yield
#                 yield
#                 yield
#                 yield

#         sim.add_sync_process(out_proc)
#         with sim.write_vcd("drv.vcd", "drv.gtkw", traces=[p.pdm_in, p.pdm_out]):
#             sim.run()
#     else:
#         plat = ChubbyHat_V01Platform()
#         plat.build(Top(gamma=args.g), do_program=True)
