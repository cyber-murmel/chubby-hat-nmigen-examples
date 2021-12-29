import argparse
from .blink import Blinker, Top
from nmigen.sim import Simulator
from nmigen_boards.chubbyhat_v0_1 import ChubbyHat_V01Platform

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true", help="Simulate PDMDriver (for debugging).")
    parser.add_argument("-g", type=float, default=2.2, help="Gamma exponent (default 2.2)")
    args = parser.parse_args()

    if args.s:
        p = Blinker(8)
        sim = Simulator(p)
        sim.add_clock(1.0 / 12e6)

        def out_proc():
            for i in range(256):
                yield

        sim.add_sync_process(out_proc)
        with sim.write_vcd("drv.vcd", "drv.gtkw", traces=[p.blink_out]):
            sim.run()
    else:
        plat = ChubbyHat_V01Platform()
        plat.build(Top(int(2.5e6)), do_program=True)
