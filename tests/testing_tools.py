import shutil
import os
import random

def config_file_content(game, profile='profile_1', extra="None"):
    content = f"I am a config file for {game}. I use {profile}. Extra info: {extra}"
    return content

def get_file_content(path):
    with open(path) as file:
        content = file.read()
    return content

def create_test_env(path, data_dir_status, game_amount):
    """
    Takes in a path (usually tmp_path from pytest) and some 
    parameters creates a testing directory tailored for the 
    specific test.
    Parameters:
    - data_dir_status (str): whether the data directory doesn't 
    exist ("no_data_dir") or exists but is empty ("empty_data_dir").
    - game_amount (int): amount of test games
    """
    
    # Create data directory
    if data_dir_status == "empty_data_dir":  # Yes I know I should use booleans, this had more options before and I don't want to go trough all my tests and change it
        os.makedirs(f"{path}/data/game_paths", exist_ok=True) 
        os.makedirs(f"{path}/data/saved_profiles", exist_ok=True)
        
    # Create games
    for i in range(1, game_amount+1):
        game = f"game_{i}"

        os.mkdir(f"{path}/{game}")  # Create game directory
        os.mkdir(f"{path}/{game}/nonconfig_dir")  # Create a non-config dir
        os.mkdir(f"{path}/{game}/config_dir")  # Create a config dir
        
        # Put some stuff into non config files
        nonconfig_file_content = "I am a random file, please leave me alone"
        with open(f"{path}/{game}/nonconfig_dir/nonconfig_file", "w") as random_nested_file:
            random_nested_file.write(nonconfig_file_content)
        with open(f"{path}/{game}/nonconfig_file", "w") as random_file:
            random_file.write(nonconfig_file_content)
            
        # Put some stuff into config files
        with open(f"{path}/{game}/config_dir/config_file", "w") as nested_config_file:
            nested_config_file.write(config_file_content(game, extra="nested"))
        with open(f"{path}/{game}/config_file", "w") as config_file:
            config_file.write(config_file_content(game))
        with open(f"{path}/{game}/another_config_file", "w") as another_config_file:
            another_config_file.write(config_file_content(game, extra="another"))
            
    """
    The final structure may look something like this:
    {path}/
    |- game_1/
       |- config_dir/
          |- config_file
       |- config_file
       |- another_config_file
    |- data/
       |- game_paths
       |- saved_profiles
       
    This would be achieved with the arguments data_dir_status='empty_data_dir' and game_amount=1
    """

# def modify_test_env(path, changes):
#     """
#     Modifies a test environment with the path 'path' and applies changes described in 'changes'.
#     'changes' should be a dictionary with paths as keys and file contents (strings) as values. If 
#     a value is a dictionary it will be considered a directory and all files inside it will be 
#     created and the contents will be applied as described above. Already existing files will not 
#     be removed.
#     """
#
#     for name in changes.keys():
#         if isinstance(name, str):
#             with open(f"{path}/{name}", "w") as file:
#                 file.write(changes[name])
#         elif isinstance(name, dict):
#             modify_test_env(f"{path}/{name}", changes[name])

def corrupt_file(path):
    """Puts random content into a given file. Used to test 'load_profile'"""
    with open(path, "w") as file:
        for i in range(100):
            char = chr(random.randint(32, 126))
            file.write(char)