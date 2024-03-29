import argparse
from game_setting_manager import save_and_load


# Create a parser to parse command-line arguments
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# Create a parser for the "save" command
parser_save = subparsers.add_parser('save', help='Save game settings to a profile')
parser_save.add_argument('game_name', help='Name of the game')
parser_save.add_argument('profile_name', help='Name of the profile') 
parser_save.add_argument('--path', nargs='+', help='Path to configuration files of the game', default=None)  # Use "--path /path/to/config/file" if the path of the game isn't saved already
parser_save.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=save_and_load.DEFAULT_DATA_PATH)
parser_save.add_argument('--overwrite-saved-profiles', help='Whether to overwrite saved profiles if they already exist', default='ask')

# Create a parser for the "load" command
parser_load = subparsers.add_parser('load', help='Load game settings from a profile')
parser_load.add_argument('game_name', help='Name of the game')
parser_load.add_argument('profile_name', help='Name of the profile')
# --path isn't needed because the game must be saved already anyway. If it isn't the program will throw an error
parser_load.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=save_and_load.DEFAULT_DATA_PATH)
# --overwrite-saved-profiles isn't needed either because this doesn't modify the data directory in any way

# Main function
def main():
    args = parser.parse_args()
    if args.command == 'save':
        try:
            save_and_load.save_profile(args.game_name, args.profile_name, args.path, args.data_path, args.overwrite_saved_profiles)
        except save_and_load.PathError as e:
            print(e.message)
        except save_and_load.DataError as e:
            print(e.message)
    elif args.command == 'load':
        try:
            save_and_load.load_profile(args.game_name, args.profile_name, args.data_path)
        except save_and_load.PathError as e:
            print(e.message)
        except save_and_load.DataError as e:
            print(e.message)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()