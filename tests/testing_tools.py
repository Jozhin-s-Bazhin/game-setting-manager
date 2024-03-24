import shutil
import os

CONFIG_FILE_CONTENT = "I am a config file for game_1. I use profile_1"
NESTED_CONFIG_FILE_CONTENT = "I am a nested config file for game_1. I use profile_1"

def config_file_content(game, nested=False, profile='profile_1'):
    content = f"I am a {'nested ' if nested else ''}config file for {game}. I use {profile}"
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
    exist ("no_data_dir"), exists but is empty ("empty_data_dir")
    or has a certain content ("{path to contents}").
    - game_amount (int): amount of test games
    """
    
    # Create data directory
    if data_dir_status == "empty_data_dir":
        os.makedirs(f"{path}/data/game_paths", exist_ok=True) 
        os.makedirs(f"{path}/data/saved_profiles", exist_ok=True)
    elif data_dir_status == "no_data_dir":
        pass 
    else:
        shutil.copytree(data_dir_status, f"{path}/data/")
        
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
            nested_config_file.write(config_file_content(game, nested=True))
        with open(f"{path}/{game}/config_file", "w") as config_file:
            config_file.write(config_file_content(game))
            
    """
    The final structure may look something like this:
    {path}/
    |- game_1/
       |- config_dir/
          |- config_file
       |- config_file
    |- data/
       |- game_paths
       |- saved_profiles
       
    This would be achieved with the arguments data_dir_status='empty_data_dir' and game_amount=1
    """