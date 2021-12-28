{pkgs ? import <nixpkgs> {}}:

with pkgs;
let
  # Python with packages
  nmigen-boards-git = python3Packages.nmigen-boards.overrideAttrs (old: {
      src = fetchFromGitHub {
        owner = "cyber-murmel";
        repo = "nmigen-boards";
        rev = "a936b6ce74b1e1d14f9d2abf10fa558586311218";
        sha256 = "04h0z6v9b0s0shmkskih4gdv8gc0rll7s3dbsn26vi5rkg1fwjzm";
      };
    });
  my-python-packages = python-packages: with python-packages; [
    nmigen
    nmigen-boards-git
  ];
  python-with-my-packages = python3.withPackages my-python-packages;
in
mkShell {
  buildInputs = [
    yosys nextpnr trellis openfpgaloader gtkwave
    python-with-my-packages
  ];
}
