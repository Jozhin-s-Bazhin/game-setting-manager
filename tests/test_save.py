import pytest
import testing_tools
import os
from save_and_load import save_profile, hash_path


# Tests that should work
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
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/another_config_file"], f"{tmp_path}/data", False)  # Run function

    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    another_file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/another_config_file')}")
    assert file_content == testing_tools.config_file_content("game_1") and another_file_content == testing_tools.config_file_content("game_1", extra="another")
    
def test_save_multiple_files_with_identical_names(tmp_path):
    """Tests whether you can save multiple files with identical names for a single profile with one game present and all data directories already created"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/config_dir/config_file"], f"{tmp_path}/data", False)  # Run function

    file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_file')}")
    nested_file_content = testing_tools.get_file_content(f"{tmp_path}/data/saved_profiles/game_1/profile_1/{hash_path(f'{tmp_path}/game_1/config_dir/config_file')}")
    assert file_content == testing_tools.config_file_content("game_1") and nested_file_content == testing_tools.config_file_content("game_1", extra="nested")
   
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
    
# Tests that should trigger an error
NO_PATHS_SPECIFIED_ERROR = "No saved paths were found at"  # The error will be different each time but should always contain this

def test_save_no_saved_game(tmp_path):
    """Tests whether trying to save a game without the data directory and no path specified will trigger the correct error."""
    testing_tools.create_test_env(tmp_path, "no_data_dir", 1)
    with pytest.raises(FileNotFoundError) as exception_info:
        save_profile("game_1", "profile_1", [], f"{tmp_path}/data", False)
    
    assert NO_PATHS_SPECIFIED_ERROR in str(exception_info.value)  
    
def test_save_no_saved_game_empty_data_dir(tmp_path):
    """Tests whether trying to save a game with an empty data directory and no path specified will trigger the correct error"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    with pytest.raises(FileNotFoundError) as exception_info:
        save_profile("game_1", "profile_1", [], f"{tmp_path}/data", False)
    
    assert NO_PATHS_SPECIFIED_ERROR in str(exception_info.value)
    
def test_save_no_saved_game_empty_list_in_path_file(tmp_path):
    """Tests whether trying to save a game with an empty list in the path file in the data_dir and no path specified will trigger the correct error"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)

    # Put empty list into path file
    with open(f"{tmp_path}/data/game_paths/game_1.json", "w") as file:
        file.write("[]")
        
    # The test itself
    with pytest.raises(ValueError) as exception_info:
        save_profile("game_1", "profile_1", [], f"{tmp_path}/data", False)
    
    assert NO_PATHS_SPECIFIED_ERROR in str(exception_info.value)
    
def test_save_no_saved_game_empty_path_file(tmp_path):
    """Tests whether trying to save a game with an empty path file in the data_dir and no path specified will trigger the correct error"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)

    # Put empty list into path file
    with open(f"{tmp_path}/data/game_paths/game_1.json", "w") as file:
        file.write    # Put empty list into path file
    with open(f"{tmp_path}/data/game_paths/game_1.json", "w") as file:
        file.write("")
       
    # The test itself
    with pytest.raises(ValueError) as exception_info:
        save_profile("game_1", "profile_1", [], f"{tmp_path}/data", False)
   
    assert "does not contain valid JSON" in str(exception_info.value)

def test_save_corrupted_path_file(tmp_path):
    """Tests whether trying to save a game with a corrupted path file in the data_dir and no path specified will trigger the correct error"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)

    # Corrupt path file
    testing_tools.corrupt_file(f"{tmp_path}/data/game_paths/game_1.json")
       
    # The test itself
    with pytest.raises(ValueError) as exception_info:
        save_profile("game_1", "profile_1", [], f"{tmp_path}/data", False)
   
    assert "does not contain valid JSON" in str(exception_info.value)