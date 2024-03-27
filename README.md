# game-setting-manager
An overengeneered cli and tui utility to save and restore setting profiles for games. 

## Installation for dev environment
### Prerequisites
- [Install Nix](https://nixos.org/download.html).
- [Enable flakes](https://nixos.wiki/wiki/Flakes)
- [Install direnv](https://direnv.net/docs/installation.html)
- You can also choose to manually run `nix develop` instead of using `direnv` to enter a shell with all the dependencies installed.

### Setup
```
git clone git@github.com:Jozhin-s-Bazhin/game-setting-manager.git
cd game-setting-manager
direnv allow  # Allow direnv to load project environment. Remove this when using nix develop.
```
