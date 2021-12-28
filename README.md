# Chubby Hat [nMigen](https://github.com/m-labs/nmigen) Examples

## Setup
You need to install `yosys`, `nextpnr`, `trellis`, `openfpgaloader` and `gtkwave`.
Use virtualenv to install the Python packaged from the `requirements.txt`.
```bash=
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip --requirement requirements.txt
```

### Nix
If you are using Nix or NixOS, you can simply run `nix shell` in the root of this repository to enter a development environment.

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
