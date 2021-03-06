![](https://raw.githubusercontent.com/cyber-murmel/chubby-hat-nmigen-examples/assets/banner.png)

# Chubby Hat [nMigen](https://github.com/m-labs/nmigen) Examples

## Setup
Use virtualenv to install the Python packages from the `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip --requirement requirements.txt
```

Additionally you need to install [`yosys`](http://yosyshq.net/yosys/download.html), [`nextpnr`](https://github.com/YosysHQ/nextpnr), [`trellis`](https://github.com/YosysHQ/prjtrellis), [`openfpgaloader`](https://trabucayre.github.io/openFPGALoader/guide/install.html) and [`gtkwave`](http://gtkwave.sourceforge.net/).

For formal verification you also need [`symbiyosys`](https://symbiyosys.readthedocs.io/en/latest/install.html), [`boolector`](https://github.com/Boolector/boolector) and [`yices`](https://yices.csl.sri.com/).

### Nix
If you are using Nix or NixOS, you can simply run `nix shell` in the root of this repository to enter a development shell.

## Getting Started
The directories in this repository are executable python modules. They can be run with `python -m <dir_name>`.
Add `-h` to get a helpt text printed.
```bash
$ python -m pdm_fade_gamma -h
usage: __main__.py [-h] [-g G] {generate,simulate} ...

positional arguments:
  {generate,simulate}
    generate           generate RTLIL, Verilog or CXXRTL from the design
    simulate           simulate the design

optional arguments:
  -h, --help           show this help message and exit
  -g G                 Gamma exponent (default 2.2)
```

### Simulation
The modules in this repository use the `main_parser` and `main_runner` from nMigen.
Star a simulation with the `simulate` command when calling a module.
To get a time scale that is equivalent to the Colorlight, set the clock period to 0.00000004s (25MHz).
You can view the file with GTKWave

```bash
python -m blink --blink-freq 2500000 simulate --vcd-file sim.vcd --gtkw-file sim.gtkw -p 0.00000004 -c 100
gtkwave sim.gtkw
```

![](https://raw.githubusercontent.com/cyber-murmel/chubby-hat-nmigen-examples/assets/blink-sim.png)

### Unit Tests and Formal Verification
We use nMigens `FHDLTestCase` class which is based on Python unit tests.
Some modules implement a formal description of their behaviour, which can be verified.
You can invoke this by running the unittest module with the other module as argument.

```bash
python -m unittest blink
```

### Programming
To write a synthesized module to the FPGA, call the module without any command.

```bash
python -m blink
```
