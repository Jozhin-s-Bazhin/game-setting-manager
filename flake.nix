{
  description = "A minimal Python environment with direnv integration";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        poetryEnv = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            poetry
            python3Packages.pytest
            poetryEnv
          ];

          shellHook = ''
            poetry install
            source "$(poetry env info --path)/bin/activate"
          '';
        };
        packages.default = poetryEnv;
        defaultPackage = poetryEnv;
        apps.default = {
          type = "app";
          program = "${poetryEnv}/bin/gsm-cli";
        };
      }
    );
}
