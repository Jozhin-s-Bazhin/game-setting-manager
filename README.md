# game-setting-saver
A tui utility to save and restore setting profiles for games.

## Installation for dev environment
### Prerequisites
- [Install Nix](https://nixos.org/download.html).
- (Optional but recommended) Install direnv if you want to have all dependencies installed automatically when entering the directory of the project.
  - [Enable flakes](https://nixos.wiki/wiki/Flakes)
  - For NixOS users: add `direnv` to your `environment.systemPackages` in your configuration.nix and add `eval $(direnv hook <your shell>)` and replace `\<your shell\>` with your shell, usually bash.
  - For non-NixOS users: install `direnv` using your system package manager, for example `sudo apt install direnv` for Debian-based systems.
  - You can also choose to manually run `nix develop` instead of using `direnv` to enter a shell with all the dependencies installed.

### Setup
```
git clone git@github.com:Jozhin-s-Bazhin/game-setting-saver.git
cd game-setting-saver
direnv allow  # Allow direnv to load project environment. Remove this when using nix develop.
```
