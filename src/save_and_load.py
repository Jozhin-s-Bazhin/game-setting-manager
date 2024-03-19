import argparse
import os


default_data_path = os.path.join(os.path.expanduser("~"), ".game_profile_data")

def check_dir(dir):
    """Check if a directory exists and create it if it doesn't"""
    if not os.path.exists(dir):
        os.mkdir(dir)

def save_profile(game, profile, paths, data_path):  # Save one or more config files to a profile to use later
    """Save a list of files to the """
    check_dir(data_path)

    path_info = f"{data_path}/game_paths/{game}.json"  # This is where the data about the paths to all config files of a particular game is stored
    check_dir(path_info)
        
    with open(path_info, "w")
    if paths:  # Check if paths are specified, else try to find paths in data dir
        for path in paths:  # Check if all paths exist
            if not os.path.exists(path):
                raise FileNotFoundError(f"{path} does not exist.")
    else:

def load_profile(game, profile, data_path):  # Load profiles saved earlier
    pass
    
# Create a parser to parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_subparsers(dest="command")

# Create a parser for the "save" command
parser_save = subparsers.add_parser('save', help='Save game settings to a profile')
parser_save.add_argument('game_name', help='Name of the game')
parser_save.add_argument('profile_name', help='Name of the profile') 
parser_save.add_argument('--path', nargs='+', help='Path to configuration file', default=None)  # Use "--path /path/to/config/file" if the path of the game isn't saved already
parser_save.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=default_data_path)

# Create a parser for the "load" command
parser_load = subparsers.add_parser('save', help='Load game settings')
parser_load.add_argument('game_name', help='Name of the game')
parser_load.add_argument('profile_name', help='Name of the profile')
# --path isn't needed because the game must be saved already anyway. If it isn't the program will throw an error
parser_load.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=default_data_path)