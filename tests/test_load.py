import pytest
import testing_tools
from save_and_load import save_profile, load_profile, hash_path


def test_load(tmp_path):
    """Test loading a profile from a single file with one game present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False)  # I didn't find any other way to save data
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")
    
    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_load_with_multipe_games(tmp_path):
    """Test loading a profile from a single file with multiple games present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 3)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data", False) 
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")

    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    assert file_content == testing_tools.config_file_content("game_1")
    
def test_load_multiple_files(tmp_path):
    """Test loading a profile from multiple files with one game present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/another_config_file"], f"{tmp_path}/data", False)  
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    testing_tools.corrupt_file(f"{tmp_path}/game_1/another_config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")

    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    another_file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/another_config_file")
    assert file_content == testing_tools.config_file_content("game_1") and another_file_content == testing_tools.config_file_content("game_1", extra="another")
    
def test_load_with_multiple_files_with_identical_names(tmp_path):
    """Test loading a profile from multiple files with identical names with one game present"""
    testing_tools.create_test_env(tmp_path, "empty_data_dir", 1)
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file", f"{tmp_path}/game_1/config_dir/config_file"], f"{tmp_path}/data", False)  
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_file")
    testing_tools.corrupt_file(f"{tmp_path}/game_1/config_dir/config_file")
    load_profile("game_1", "profile_1", f"{tmp_path}/data")

    file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_file")
    nested_file_content = testing_tools.get_file_content(f"{tmp_path}/game_1/config_dir/config_file")
    assert file_content == testing_tools.config_file_content("game_1") and nested_file_content == testing_tools.config_file_content("game_1", extra="nested")
 
# test_load_no_data_dir()
# load_multiple_games()

# tests that should trigger an error

# test_no_saved_game
# test_no_saved_game_empty_data_dir
# test_no_saved_game_empty_list_in_path_file
# test_no_saved_game_empty_path_file
# test_no_saved_game_corrupted_path_file