import argparse
from src.commands import events, starred_command, issues_command

def setup_parser():
    parser = argparse.ArgumentParser(
        prog="GitHub User Activity",
        description="CLI tool to retrieve information from the GitHub API"
    )

    subparser = parser.add_subparsers(dest="command", required=True)

    username_parser = subparser.add_parser("events", help="Fetch events")
    username_parser.add_argument("username", type=str, help="retrieves all information without filters")
    username_parser.add_argument("-l", "--limit", type=int, default=30, help="return a specified number of most recent events")
    username_parser.add_argument("-c", "--commits", action='store_true', help="retrieves only commit history")
    # username_parser.add_argument("-s", "--starred", action='store_true', help="retrieves number of repos the user has starred")
    # username_parser.add_argument("-i", "--issues", action='store_true', help="retrieves number of issues the user has open")
    username_parser.set_defaults(func=events)

    starred_parser = subparser.add_parser("starred", help="retrieves starred repos")
    starred_parser.add_argument("username", help="retrieves repos starred by user")
    starred_parser.set_defaults(func=starred_command)

    issues_parser = subparser.add_parser("issues", help="retrieves open issues by user")
    issues_parser.add_argument("username", help="retrieves open issues by user")
    issues_parser.set_defaults(func=issues_command)

    return parser
