import pytest
import shutil
from create_test_env import create_test_env
from game_setting_manager.save_and_load import save_profile

def test_save(tmp_path):
    """Tests whether you can save a single profile with all data directories already created"""
    create_test_env(tmp_path, "empty_data_dir", 1)  # Create testing environment with one game and an empty data directory
    save_profile("game_1", "profile_1", [f"{tmp_path}/game_1/config_file"], f"{tmp_path}/data")