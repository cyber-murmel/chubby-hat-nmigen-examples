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
