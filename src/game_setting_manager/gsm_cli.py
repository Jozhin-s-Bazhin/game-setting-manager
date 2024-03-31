import argparse
from game_setting_manager import save_and_load


def add_common_args(subparser):
    """Adds common argument to a given subparser (parser_save and parser_load)"""
    subparser.add_argument('game_name', help='Name of the game')
    subparser.add_argument('profile_name', help='Name of the profile')
    subparser.add_argument('--data-path', help='Path to saved data, mostly intended for testing', default=save_and_load.DEFAULT_DATA_PATH)

# Create a parser to parse command-line arguments
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# Save parser
parser_save = subparsers.add_parser('save', help='Save game settings to a profile')
parser_save.add_argument('--path', nargs='+', help='Path to configuration files of the game', default=None)  # Use "--path /path/to/config/file" if the path of the game isn't saved already
add_common_args(parser_save)

# Load parser
parser_load = subparsers.add_parser('load', help='Load game settings from a profile')
add_common_args(parser_load)

# Main function
def main():
    args = parser.parse_args()
    if args.command == 'save':
        try:
            save_and_load.save_profile(args.game_name, args.profile_name, args.path, args.data_path, args.overwrite_saved_profiles)
        except ( save_and_load.PathError, save_and_load.DataError ) as e:
            print(e.message)
    elif args.command == 'load':
        try:
            save_and_load.load_profile(args.game_name, args.profile_name, args.data_path)
        except ( save_and_load.PathError, save_and_load.DataError ) as e:
            print(e.message)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()