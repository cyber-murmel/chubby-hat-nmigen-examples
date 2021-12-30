# Chubby Hat [nMigen](https://github.com/m-labs/nmigen) Examples

## Setup
Use virtualenv to install the Python packaged from the `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip --requirement requirements.txt
```

Additionally you need to install [`yosys`](http://yosyshq.net/yosys/download.html), [`nextpnr`](https://github.com/YosysHQ/nextpnr), [`trellis`](https://github.com/YosysHQ/prjtrellis), [`openfpgaloader`](https://trabucayre.github.io/openFPGALoader/guide/install.html) and [`gtkwave`](http://gtkwave.sourceforge.net/).

For formal verification you also need [`symbiyosys`](https://symbiyosys.readthedocs.io/en/latest/install.html) and [`boolector`](https://github.com/Boolector/boolector).

### Nix
If you are using Nix or NixOS, you can simply run `nix shell` in the root of this repository to enter a development shell.

## Getting Started
The directories in this repository are executable python modules. They can be run with `python -m <dir_name>`.
Add `-h` to get a helpt text printed.
```bash
$ python -m pdm_fade_gamma -h
usage: __main__.py [-h] [-s] [-g G]

optional arguments:
  -h, --help  show this help message and exit
  -s          Simulate PDMDriver (for debugging).
  -g G        Gamma exponent (default 2.2)

$ python -m pdm_fade_gamma -s

$ gtkwave drv.gtkw
```
If no futher argument is supplied, the module in the directory gets synthesized and programmed to the chubby hat.
```bash
$ python -m pdm_fade_gamma
```

## Formal Verification
Some modules implement a formal description of their behaviour, which can be verified. To to this, generate the intermediate language (`.il`) representation for the module and run it with the `.sby` script from that module.

For example:
```bash
python -m blink generate -t il > toplevel.il
sby -f blink/cover_bmc.sby
```
