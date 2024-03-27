{
  description = "A minimal Python environment with direnv integration";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            poetry
            python3Packages.pytest
          ];

          shellHook = ''
            poetry install
            source "$(poetry env info --path)/bin/activate"
          '';
        };
        packages = {
          gsm-cli = mkPoetryApplication { projectDir = self; };
          default = self.packages.${system}.gsm-cli;
        };        
      }
    );
}
