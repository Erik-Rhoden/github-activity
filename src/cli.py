import argparse
from src.commands import foo

def setup_parser():
    parser = argparse.ArgumentParser(
        prog="GitHub User Activity",
        description="CLI tool to retrieve information from the GitHub API"
    )
    # subparsers = parser.add_subparsers(dest="command", required=True)

    parser.add_argument("username", help="GitHub username")
    parser.set_defaults(func=foo)

    return parser
