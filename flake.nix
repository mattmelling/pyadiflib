{
  outputs = { nixpkgs, ... }:
    let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      python-env = pkgs.python3.withPackages (ps: with ps; [
        pytest
      ]);
    in {
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = with pkgs; [
          python-env
        ];
      };
    };
}
