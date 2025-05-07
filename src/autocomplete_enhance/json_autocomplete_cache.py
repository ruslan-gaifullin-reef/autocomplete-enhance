import argparse

# from autocomplete_enhance.sample_cli.heavy import parser
from autocomplete_enhance.sample_cli.describe_github_user import parser
import json

# save the parser to a json file


def extract_parser_structure(parser):
    parser_structure = {
        "description": parser.description,
        "arguments": [],
        "subparsers": {}
    }

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            for sub_name, sub_parser in action.choices.items():
                parser_structure["subparsers"][sub_name] = extract_parser_structure(sub_parser)
        elif not isinstance(action, argparse._HelpAction):
            arg_info = {
                "option_strings": action.option_strings,
                "dest": action.dest,
                "help": action.help,
                "required": action.required,
                "nargs": action.nargs,
                "default": action.default,
                "type": str(action.type) if action.type else None,
                "choices": list(action.choices) if action.choices else None,
                "metavar": action.metavar,
                "completer": action.completer.__name__ if hasattr(action, 'completer') else None,
            }
            parser_structure["arguments"].append(arg_info)

    return parser_structure

def save_parser_to_json(arg_parser: argparse.ArgumentParser, filename: str):
    """
    Save the parser command structure, and its arguments to a json file.
    Descend into subparsers and save their structure as well.
    """
    structure = extract_parser_structure(arg_parser)
    with open(filename, 'w') as f:
        json.dump(structure, f, indent=4)


if __name__ == '__main__':
    # save the parser to a json file
    save_parser_to_json(parser, 'parser.json')
