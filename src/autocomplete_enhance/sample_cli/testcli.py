#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse

import argcomplete

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--foo", choices=["a", "b", "c"])

    argcomplete.autocomplete(parser)

    args = parser.parse_args()


if __name__ == '__main__':
    main()
