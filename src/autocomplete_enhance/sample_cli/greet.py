#!/usr/bin/env python
import argparse
import argcomplete
from argcomplete.completers import ChoicesCompleter

def greet(args):
    print(f"Hello, {args.name}!")

def calculate(args):
    if args.operation == 'add':
        result = args.x + args.y
    elif args.operation == 'subtract':
        result = args.x - args.y
    else:
        raise ValueError("Unsupported operation")
    print(f"Result: {result}")

def main():
    parser = argparse.ArgumentParser(description="Sample CLI with argcomplete")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Greet command
    greet_parser = subparsers.add_parser('greet', help="Greet someone")
    greet_parser.add_argument('name', help="Name of the person")
    greet_parser.set_defaults(func=greet)

    # Calculate command
    calc_parser = subparsers.add_parser('calculate', help="Perform a calculation")
    calc_parser.add_argument('x', type=int, help="First number")
    calc_parser.add_argument('y', type=int, help="Second number")
    calc_parser.add_argument(
        'operation',
        choices=['add', 'subtract'],
        help="Operation to perform"
    ).completer = ChoicesCompleter(['add', 'subtract'])
    calc_parser.set_defaults(func=calculate)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
