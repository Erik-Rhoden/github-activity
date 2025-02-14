import http.client
import json
import socket

def get_data(args):
    try:
        socket.getaddrinfo("api.github.com", 443)
    except socket.gaierror:
        print("Network error: Unable to resolve host. Check your internet connection.")
        return []
    
    try:
        github_api = "api.github.com"
        endpoint = f"/users/{args.username}/{args.command}"
        header = {"User-Agent" : "github-cli-fetcher",
                "Accept": "application/vnd.github.v3+json"
                }

        conn = http.client.HTTPSConnection(github_api, timeout=2)
        try:
            conn.request("GET", endpoint, headers=header)
            response = conn.getresponse()

            if response.status == 403:
                print("Rate Limit Exceeded! Try again later.")
                return {}
            if response.status != 200:
                print(f"Github API returned status {response.status}")
                return {}

            data = response.read()
            return json.loads(data.decode("utf-8"))
        finally:
            conn.close()

    except (http.client.HTTPException, TimeoutError, socket.timeout) as e:
        print(f"Network or HTTP error: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return {}

def events(args):
    events = get_data(args)

    limit = args.limit
    if args.commits:
        pushed_commits(args, limit, events)
        return
    
    repos = pushed_commits(args, limit, events)
    if repos:
        print(f'Output:')
    for repo, count in repos.items():
        print(f'- Pushed {count} to {repo}')
    issues = issues_open(args)
    for issue in issues:
        print(f'- Opened a new issue in {issue}')
    starred = starred_repos(args)
    for star in starred:
        print(f'- Starred {star}')

def pushed_commits(args, limit, events):
    count = 0
    repo = ""
    repo_dict = {}

    for event in events:
        if event.get("type") == "PushEvent" and count < limit:
            repo = event['repo']['name']
            count += 1
            if repo not in repo_dict:
                repo_dict[repo] = 0
            repo_dict[repo] += 1
    
    if not args.commits:
        return repo_dict
    for repo in repo_dict:
        print(f'- Pushed {repo_dict[repo]} to {repo}') 
        
def starred_repos(args):
    original_command = args.command
    if args.command == 'events':
        args.command = 'starred'
    
    stars = get_data(args)

    args.command = original_command  

    if not stars:
        return [] if original_command == "events" else print("No repos have been starred")

    starred = [star["full_name"] for star in stars]

    if original_command == "events":
        return starred
    
    for star in starred:
        print(f"- Starred {star}")

def issues_open(args):
    try:
        socket.getaddrinfo("api.github.com", 443)
    except socket.gaierror:
        print("Network error: Unable to resolve host. Check your internet connection.")
        return []
    
    try:
        github_api = "api.github.com"
        endpoint = f"/search/issues?q=author:{args.username}+type:issue+state:open"
        header = {"User-Agent" : "github-cli-fetcher",
                "Accept": "application/vnd.github.v3+json"
                }
        
        conn = http.client.HTTPSConnection(github_api, timeout=2)
        try:
            conn.request("GET", endpoint, headers=header)

            response = conn.getresponse()

            if response.status != 200:
                print(f"GitHub API returned status {response.status}")
                return []

            data = response.read()
            results = json.loads(data.decode("utf-8"))
        
            items = results.get('items', [])

            if args.command == 'events':
                return items

            if not items:
                print("no open issues")
                return
            
            for item in items:
                repo_url = item.get("repository_url", "")
                repo_name = "/".join(repo_url.split("/")[-2:]) if repo_url else "Unknown Repo"
                print(f'- Opened a new issue in {repo_name}')
        finally:
            conn.close()

    except (http.client.HTTPException, TimeoutError, socket.timeout) as e:
        print(f"Network or HTTP error: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return {}
