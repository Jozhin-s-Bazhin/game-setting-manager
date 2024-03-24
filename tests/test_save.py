import pytest
import testing_tools
from save_and_load import save_profile, hash_path


def test_save(tmp_path):
    """Tests whether you can save a single profile with one game present and all data directories already created"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  
    
    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_save_with_multiple_games(tmp_path):
    """Tests whether you can save a single profile with multiple games present and all data directories already created"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 3)  # Create testing environment with three games and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False) 
    
    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_save_multiple_files(tmp_path):
    """Tests whether you can save multiple files for a single profile with one game present and all data directories already created"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/config_dir/config_file"], f"{tmp_path}/data", False)  # Run function

    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    nested_file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_dir/config_file')}")
    assert file_content == testing_tools.config_file_content("game_1") and nested_file_content == testing_tools.config_file_content("game_1", nested=True)
   
def test_save_no_data_dir(tmp_path):
    """Tests whether you can save a single profile with one game present and no data directories created"""
    testing_tools.create_test_env(tmp_path, "no_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  
    
    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_save_full_data_dir(tmp_path):
    """Tests whether you can save a single profile with one game present and a saved profile and path data already present in the data directory"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  # Run function to create data inside the data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", True)  # Run function to test it

    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_save_multiple_games(tmp_path):
    """Tests whether you can save multiple profiles for multiple games with an empty data directory"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 2)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)
    save_profile("game_2", "profile_1", [f"{tmp_path}/game_2/config_file"], f"{tmp_path}/data", False)
    
    game_1_file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    game_2_file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_2/profile_1/{hash_path(f'{tmp_path}/game_2/config_file')}")
    assert game_1_file_content == testing_tools.config_file_content("game_1") and game_2_file_content == testing_tools.config_file_content("game_2")