import argparse
import os
import shutil
import sys
import json
import hashlib


default_data_path = os.path.join(os.path.expanduser("~"), ".game_setting_manager")

def hash_path(file_path):
    """Takes a string and returns a hash. Used here to hash file paths"""
    encoded_path = file_path.encode('utf-8')
    hasher = hashlib.md5()
    hasher.update(encoded_path)
    return hasher.hexdigest()

def save_profile(game, profile, paths, data_path):  
    """Saves all files specified in 'paths' or read from '<data_path>/game_paths/<game>.json' to '<data_path>/<game>/<profile>/'"""

    # Check if there are any provided paths to game's files
    if not os.path.exists(data_path): 
        raise ValueError(f"{data_path} has not been found")

    # Check and create file with path info an data directory
    os.makedirs(f"{data_path}/game_paths/", exist_ok=True)  # This is where all the data about config paths is stored
    
    # Check if paths are specified, else try to find paths in data dir
    config_file_path_info = f"{data_path}/game_paths/{game}.json"  # Path to file containing a list of all configuration files of the game
    if paths:  
        # Check if all paths exist
        for path in paths: 
            if not os.path.exists(path):
                raise FileNotFoundError(f"{path} does not exist.")
            
        # Add path entries into the path list of the game
        if os.path.exists(config_file_path_info):
            if input("Are you sure you want to overwrite your current path list? Enter 'yes' to proceed.\n").strip() != "yes":
                print("Exiting")
                sys.exit()
        
        absolute_paths = [os.path.abspath(path) for path in paths] # Convert all relative paths to absolute
        with open(config_file_path_info, "w") as file: 
            json.dump(paths, file)
    else:
        with open(config_file_path_info, "r") as file:
            paths = json.load(file)
            
    # Check the directory where saved profiles are stored and copy the games config files to it
    profile_path = f"{data_path}/{game}/{profile}/"
    os.makedirs(profile_path, exist_ok=True)
    for path in paths:
        shutil.copy(path, f"{profile_path}/{hash_path(path)}")

def load_profile(game, profile, data_path):  
    """Loads all files from '<data_path>/<game>/<profile>/' to the appropriate locations read from '<data_path>/game_paths/<game>.json"""
    config_file_path_info = f"{data_path}/game_paths/{game}.json"  # Path to file containing a list of all configuration files of the game

    with open(config_file_path_info, "r") as file:
        paths = json.load(file)
        
    for path in paths:
        saved_path = f"{data_path}/{game}/{profile}/{hash_path(path)}"
        # Check if saved file exists
        if not os.path.exists(saved_path):
            raise FileNotFoundError(f"Saved path: '{saved_path}' not found.")
        shutil.copy(saved_path, path)

# Create a parser to parse command-line arguments
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# Create a parser for the "save" command
parser_save = subparsers.add_parser('save', help='Save game settings to a profile')
parser_save.add_argument('game_name', help='Name of the game')
parser_save.add_argument('profile_name', help='Name of the profile') 
parser_save.add_argument('--path', nargs='+', help='Path to configuration files of the game', default=None)  # Use "--path /path/to/config/file" if the path of the game isn't saved already
parser_save.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=default_data_path)

# Create a parser for the "load" command
parser_load = subparsers.add_parser('load', help='Load game settings from a profile')
parser_load.add_argument('game_name', help='Name of the game')
parser_load.add_argument('profile_name', help='Name of the profile')
# --path isn't needed because the game must be saved already anyway. If it isn't the program will throw an error
parser_load.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=default_data_path)

# Main function
def main():
    args = parser.parse_args()
    if args.command == 'save':
        save_profile(args.game_name, args.profile_name, args.path, args.data_path)
    elif args.command == 'load':
        load_profile(args.game_name, args.profile_name, args.data_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
