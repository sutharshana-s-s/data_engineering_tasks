import argparse
import shlex
import sys
import traceback
from data_processor import DataProcessor


class InteractiveParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"ERROR: {message}\nEnter 'help' to list available commands.")
        raise ValueError("Argparse Error")


# Sets up the argument parser with ingest, validate, and transform commands and returns the configured parser.
def setup_parser():
    parser = InteractiveParser(prog="datatool", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    ingest_parser = subparsers.add_parser("ingest", help="Ingest a dataset and show metadata")
    ingest_parser.add_argument("input_file", help="Path to input CSV or JSON file")

    validate_parser = subparsers.add_parser("validate", help="Check data quality")
    validate_parser.add_argument("input_file", help="Path to input CSV or JSON file")

    transform_parser = subparsers.add_parser("transform", help="Clean and save dataset")
    transform_parser.add_argument("input_file", help="Path to input CSV or JSON file")
    transform_parser.add_argument("output_file", help="Path to save the cleaned CSV or JSON file")

    return parser


# Displays the help message with available commands.
def display_help_message():
    help_text = (
        "\n" + "="*60 + "\n"
        "DATATOOL - DATA ENGINEERING UTILITY\n"
        "="*60 + "\n"
        "\nCOMMANDS:\n"
        "  ingest <input_file>\n"
        "    Display dataset metadata (row count, columns, data types)\n\n"
        "  validate <input_file>\n"
        "    Analyze data quality issues (nulls, duplicates, type inconsistencies)\n\n"
        "  transform <input_file> <output_file>\n"
        "    Clean dataset, remove duplicates, handle missing values, and export\n\n"
        "  help\n"
        "    Display this help message\n\n"
        "  exit\n"
        "    Close the application\n"
        "="*60 + "\n"
    )
    print(help_text)


# Handles the parsed command arguments and calls the matching DataProcessor method.
def handle_command(args):
    if args.command == "ingest":
        DataProcessor.ingest(args.input_file)
    elif args.command == "validate":
        DataProcessor.validate(args.input_file)
    elif args.command == "transform":
        DataProcessor.transform(args.input_file, args.output_file)


# Runs the interactive CLI loop and manages user commands until exit.
def run_interactive_cli():
    banner = (
        "\n" + "="*60 + "\n"
        "DATATOOL - DATA ENGINEERING UTILITY\n"
        "="*60 + "\n"
        "Enter 'help' for available commands or 'exit' to terminate.\n"
    )
    print(banner)
    parser = setup_parser()
    
    while True:
        try:
            cmd = input("datatool> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ['exit', 'quit']:
                print("\nSession terminated.\n")
                sys.exit(0)
            
            if cmd.lower() in ['help', '?', '-h', '--help']:
                display_help_message()
                continue

            args = parser.parse_args(shlex.split(cmd))
            handle_command(args)

        except ValueError:
            continue
        except KeyboardInterrupt:
            print("\n\nSession terminated.\n")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            traceback.print_exc()

