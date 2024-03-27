import os
import shutil
import sys
import json
import hashlib


DEFAULT_DATA_PATH = os.path.join(os.path.expanduser("~"), ".game_setting_manager")

# Define custom errors
class PathError(BaseException):
    """Exception raised when something goes wrong with the 'paths' variable in 'save_profile' or 'load_profile'"""
    def __init__(self, message):
        self.message = message
        
class DataError(BaseException):
    """Exception raised when something goes wrong with the data directory"""
    def __init__(self, message):
        self.message = message

def hash_path(file_path):
    """Takes a string and returns a hash. Used here to hash file paths"""
    encoded_path = file_path.encode('utf-8')
    hasher = hashlib.md5()
    hasher.update(encoded_path)
    return hasher.hexdigest()

def save_profile(game, profile, paths, data_path):  
    """Saves all files specified in 'paths' or read from '<data_path>/game_paths/<game>.json' to '<data_path>/<game>/<profile>/'"""
    config_file_path_info = f"{data_path}/game_paths/{game}.json"

    # Check if there are any provided paths to game's files
    if (not os.path.exists(config_file_path_info) and not paths): 
        raise PathError(f"No saved paths were found at '{config_file_path_info}' and no paths were specified trough --path.")

    # Check and create file with path info an data directory
    os.makedirs(f"{data_path}/game_paths/", exist_ok=True)  # This is where all the data about config paths is stored
    
    # Check if paths are specified, else try to find paths in data dir
    if paths:  
        # Check if all paths exist
        for path in paths: 
            if not os.path.exists(path):
                raise PathError(f"{path} does not exist.")
            
        # Add paths to data
        absolute_paths = [os.path.abspath(path) for path in paths] # Convert all relative paths to absolute
        with open(config_file_path_info, "w") as file: 
            json.dump(paths, file)
    else:
        try:
            with open(config_file_path_info, "r") as file:
                paths = json.load(file)
        except:
            raise DataError(f"The path file ({config_file_path_info}) does not contain valid JSON")

        # Check if file contains an empty list
        if not paths or not isinstance(paths, list):
            raise DataError(f"No saved paths were found at {config_file_path_info}")
            
    # Check the directory where saved profiles are stored and copy the games config files to it
    profile_path = f"{data_path}/saved_profiles/{game}/{profile}/"
    os.makedirs(profile_path, exist_ok=True)
    for path in paths:
        shutil.copy(path, f"{profile_path}/{hash_path(path)}")

def load_profile(game, profile, data_path):  
    """Loads all files from '<data_path>/<game>/<profile>/' to the appropriate locations read from '<data_path>/game_paths/<game>.json"""
    config_file_path_info = f"{data_path}/game_paths/{game}.json"  # Path to file containing a list of all configuration files of the game

    with open(config_file_path_info, "r") as file:
        paths = json.load(file)
        
    for path in paths:
        saved_path = f"{data_path}/saved_profiles/{game}/{profile}/{hash_path(path)}"
        # Check if saved file exists
        if not os.path.exists(saved_path):
            raise PathError(f"Saved path: '{saved_path}' not found.")
        shutil.copy(saved_path, path)
