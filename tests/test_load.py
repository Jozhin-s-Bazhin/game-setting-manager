import pytest
import testing_tools
from save_and_load import save_profile, load_profile, hash_path


def test_load(tmp_path):
    """Test loading a profile from a single file with one game present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data")  # I didn't find any other way to save data
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")
    
    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_load_with_multipe_games(tmp_path):
    """Test loading a profile from a single file with multiple games present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 3)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data") 
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")

    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_load_multiple_files(tmp_path):
    """Test loading a profile from multiple files with one game present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/another_config_file"], f"{tmp_path}/data")  
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    testing_tools.corrupt_file(f"{tmp_path}/game_1/another_config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")

    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    another_file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/another_config_file")
    assert file_content == testing_tools.config_file_content("game_1") and another_file_content == testing_tools.config_file_content("game_1", extra="another")
    
def test_load_with_multiple_files_with_identical_names(tmp_path):
    """Test loading a profile from multiple files with identical names with one game present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/config_dir/config_file"], f"{tmp_path}/data")
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_dir/config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")

    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    nested_file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_dir/config_file")
    assert file_content == testing_tools.config_file_content("game_1") and nested_file_content == testing_tools.config_file_content("game_1", extra="nested")

def load_multiple_games(tmp_path):
    """Tests loading multiple profiles from multiple different games"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 2)
    
    # Save profiles
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data")
    save_profile("game_2", "profile_1", [f"{tmp_path}/game_2/config_file"], f"{tmp_path}/data")
    
    # Corrupt original files
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    testing_tools.corrupt_file(f"{tmp_path}/game_2/config_file")
    
    # Restore files
    load_profile("game_1", "profile_1")
    load_profile("game_2", "profile_1")
    
    # Get contents of original files
    game_1_file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    game_2_file_content = testing_tools.get_file_content(f"{tmp_path}/game_2/config_file")
    
    assert game_1_file_content == testing_tools.config_file_content("game_1") and game_2_file_content == testing_tools.config_file_content("game_2")


# tests that should trigger an error

def test_load_no_data_dir(tmp_path):
    """Tests whether loading a profile from a single file with one game present and no data directories created triggers the correct error"""
    pass

def test_no_saved_game(tmp_path):
    pass 

def test_no_saved_game_empty_data_dir(tmp_path):
    pass

# test_no_saved_game_empty_list_in_path_file
# test_no_saved_game_empty_path_file
# test_no_saved_game_corrupted_path_file