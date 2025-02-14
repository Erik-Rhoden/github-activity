from src.task import events, starred_repos, issues_open

def username_command(args):
    events(args)

def starred_command(args):
    starred_repos(args)

def issues_command(args):
    issues_open(args)
