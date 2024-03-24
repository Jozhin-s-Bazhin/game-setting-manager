import pytest
import shutil
import create_test_env
from save_and_load import save_profile, hash_path


def test_save(tmp_path):
    """Tests whether you can save a single profile with one game present and all data directories already created"""
    create_test_env.create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data")  # Run function
    
    # Check if profile has been saved correctly
    with open(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}") as config_file:
        file_contents = config_file.read()
    assert file_contents == "I am a config file for game_1. I use profile_1"
    
def test_save_with_multiple_games(tmp_path):
    """Tests whether you can save a single profile with multiple games present and all data directories already created"""
    create_test_env.create_test_env(tmp_path, "empty_data_dir", 3)  # Create testing environment with three games and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data")  # Run function
    
    # Check if profile has been saved correctly
    with open(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}") as config_file:
        file_contents = config_file.read()
    assert file_contents == "I am a config file for game_1. I use profile_1"
    
def test_save_multiple_files(tmp_path):
    """Tests whether you can save multiple files for a single profile with one game present and all data directories already created"""
    create_test_env.create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/config_dir/config_file"], f"{tmp_path}/data")  # Run function

    with open(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}") as config_file:
        file_contents = config_file.read()
    with open(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_dir/config_file')}") as config_file:
        nested_file_contents = config_file.read()
        
    assert file_contents == "I am a config file for game_1. I use profile_1" and nested_file_contents == "I am a nested config file for game_1. I use profile_1"
   
def test_no_data_dir(tmp_path):
    """Tests whether you can save a single profile with one game present and no data directories created"""
    create_test_env.create_test_env(tmp_path, "no_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data")  # Run function
    
    # Check if profile has been saved correctly
    with open(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}") as config_file:
        file_contents = config_file.read()
    assert file_contents == "I am a config file for game_1. I use profile_1"