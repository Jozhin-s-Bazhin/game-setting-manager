{
  description = "A minimal Python environment with direnv integration";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            poetry
            python3Packages.pytest
          ];

          shellHook = ''
	          poetry install
	          source "$(poetry env info --path)/bin/activate"
          '';
        };
      }
    );
}

