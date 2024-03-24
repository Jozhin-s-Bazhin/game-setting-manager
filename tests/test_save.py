import pytest
import shutil
from testing_tools import get_file_content, CONFIG_FILE_CONTENT, NESTED_CONFIG_FILE_CONTENT, create_test_env
from save_and_load import save_profile, hash_path


def test_save(tmp_path):
    """Tests whether you can save a single profile with one game present and all data directories already created"""
    create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  
    
    file_content = get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == CONFIG_FILE_CONTENT
    
def test_save_with_multiple_games(tmp_path):
    """Tests whether you can save a single profile with multiple games present and all data directories already created"""
    create_test_env(tmp_path, "empty_data_dir", 3)  # Create testing environment with three games and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False) 
    
    file_content = get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == CONFIG_FILE_CONTENT
    
def test_save_multiple_files(tmp_path):
    """Tests whether you can save multiple files for a single profile with one game present and all data directories already created"""
    create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/config_dir/config_file"], f"{tmp_path}/data", False)  # Run function

    file_content = get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    nested_file_content = get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_dir/config_file')}")
    assert file_content == CONFIG_FILE_CONTENT and nested_file_content == NESTED_CONFIG_FILE_CONTENT
   
def test_no_data_dir(tmp_path):
    """Tests whether you can save a single profile with one game present and no data directories created"""
    create_test_env(tmp_path, "no_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  
    
    file_content = get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == CONFIG_FILE_CONTENT
    
def test_full_data_dir(tmp_path):
    """Tests whether you can save a single profile with one game present and a saved profile and path data already present in the data directory"""
    create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  # Run function to create data inside the data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", True)  # Run function to test it

    file_content = get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == CONFIG_FILE_CONTENT