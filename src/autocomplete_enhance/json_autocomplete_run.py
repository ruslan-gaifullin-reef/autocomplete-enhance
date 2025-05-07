#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse
import json
import os
from typing import Dict, Any

import argcomplete

PARSER_JSON_PATH = "/Users/work/proj/autocomplete-enhance/parser.json"

def github_org_members(prefix, parsed_args, **kwargs):
    return [f"{prefix}{i}" for i in range(3)]

def completer2(prefix, parsed_args, **kwargs):
    return [f"{prefix}{i}" for i in range(3, 8)]


def mock_completer(original_name):
    if not original_name:
        return None

    def completer(prefix, parsed_args, **kwargs):
        variants = [f"{original_name}_{i}" for i in range(3)]
        return [v for v in variants if v.startswith(prefix)]

    return completer


def real_completer(func_name):
    if not func_name:
        return None

    def completer(prefix, parsed_args, **kwargs):
        # import original_name from autocomplete_enhance.sample_cli.describe_github_user
        import importlib
        module_name = 'autocomplete_enhance.sample_cli.describe_github_user'
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        # Call the original completer function
        return func(prefix, parsed_args, **kwargs)

    return completer


def create_parser_from_structure(structure: Dict[str, Any]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=structure.get("description"))

    subparsers = None
    if structure.get("subparsers"):
        subparsers = parser.add_subparsers(dest="command")

    # Add arguments
    for arg in structure.get("arguments", []):
        kwargs = {
            "help": arg.get("help"),
            "required": arg.get("required", False),
            "nargs": arg.get("nargs"),
            "default": arg.get("default"),
            "choices": arg.get("choices"),
            "metavar": arg.get("metavar"),
        }

        # Convert type string back to actual type if necessary
        if arg.get("type") and arg["type"] != "None":
            if "int" in arg["type"]:
                kwargs["type"] = int
            elif "float" in arg["type"]:
                kwargs["type"] = float
            elif "str" in arg["type"]:
                kwargs["type"] = str
            # Add more types as needed

        # Clean None values from kwargs
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        option_strings = arg.get("option_strings", [])
        completer = real_completer(arg.get("completer"))
        if option_strings:
            parser.add_argument(*option_strings, **kwargs).completer = completer
        else:
            parser.add_argument(arg["dest"], **kwargs).completer = completer

    # Recurse into subparsers
    if subparsers:
        for name, sub_struct in structure["subparsers"].items():
            subparser = subparsers.add_parser(name, help=sub_struct.get("description"))
            nested_parser = create_parser_from_structure(sub_struct)
            # Copy arguments from nested parser
            for action in nested_parser._actions:
                if isinstance(action, argparse._SubParsersAction):
                    continue  # subparsers already handled recursively
                args = action.option_strings or [action.dest]
                arg_kwargs = {
                    "help": action.help,
                    "required": action.required,
                    "nargs": action.nargs,
                    "default": action.default,
                    "choices": action.choices,
                    "metavar": action.metavar,
                    "type": action.type,
                }
                arg_kwargs = {k: v for k, v in arg_kwargs.items() if v is not None}
                subparser.add_argument(*args, **arg_kwargs)

    return parser

def load_parser_from_json(filename: str) -> argparse.ArgumentParser:
    with open(filename, 'r') as f:
        structure = json.load(f)
    return create_parser_from_structure(structure)

parser = load_parser_from_json(PARSER_JSON_PATH)
argcomplete.autocomplete(parser)
args = parser.parse_args()
