import argparse
import shlex
import sys
from data_processor import DataProcessor


class InteractiveParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"ERROR: {message}\nEnter 'help' to list available commands.")
        raise ValueError("Argparse Error")


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


def display_help_message():
    print("\n" + "="*60)
    print("DATATOOL - DATA ENGINEERING UTILITY")
    print("="*60)
    print("\nCOMMANDS:\n")
    print("  ingest <input_file>")
    print("    Display dataset metadata (row count, columns, data types)\n")
    print("  validate <input_file>")
    print("    Analyze data quality issues (nulls, duplicates, type inconsistencies)\n")
    print("  transform <input_file> <output_file>")
    print("    Clean dataset, remove duplicates, handle missing values, and export\n")
    print("  help")
    print("    Display this help message\n")
    print("  exit")
    print("    Close the application\n")
    print("="*60 + "\n")


def handle_command(args):
    if args.command == "ingest":
        DataProcessor.ingest(args.input_file)
    elif args.command == "validate":
        DataProcessor.validate(args.input_file)
    elif args.command == "transform":
        DataProcessor.transform(args.input_file, args.output_file)


def run_interactive_cli():
    parser = setup_parser()
    print("\n" + "="*60)
    print("DATATOOL - DATA ENGINEERING UTILITY")
    print("="*60)
    print("Enter 'help' for available commands or 'exit' to terminate.\n")
    
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
