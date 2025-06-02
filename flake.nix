{
  outputs = { self, nixpkgs, ... }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      python-env = pkgs.python3.withPackages (ps: with ps; [
        pytest
      ]);
      pyadiflib = pkgs: pkgs.python3Packages.buildPythonPackage rec {
        name = "pyadiflib";
        format = "pyproject";
        src = ./.;
        propagatedBuildInputs = with pkgs.python3Packages; [
          pytest
          setuptools
        ];
      };
    in {
      devShell = pkgs.lib.genAttrs systems (system: let
        pkgs = import nixpkgs { inherit system; };
      in pkgs.mkShell {
        buildInputs = with pkgs; [
          python-env
        ];
      });
      packages = pkgs.lib.genAttrs systems (system: let
        pkgs = import nixpkgs { inherit system; };
      in {
        pyadiflib = pyadiflib pkgs;
      });
      defaultPackage = pkgs.lib.genAttrs systems (system: let
        pkgs = import nixpkgs { inherit system; };
      in pyadiflib pkgs);
    };
}
