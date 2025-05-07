import argcomplete

# import dill
#
# with open('cached_parser.pkl', 'wb') as f:
#     dill.dump(parser, f)

import pickle

def identity(string):
    return string

def main():
    with open('cached_parser.pkl', 'wb') as f:
        from autocomplete_enhance.sample_cli.describe_github_user import parser
        parser.register('type', None, identity)
        pickle.dump(parser, f)


if __name__ == '__main__':
    main()
