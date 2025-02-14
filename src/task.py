import http.client
import json

def get_data(args):
    github_api = "api.github.com"
    endpoint = f"/users/{args.username}/{args.command}"
    header = {"User-Agent" : "github-cli-fetcher",
              "Accept": "application/vnd.github.v3+json"
              }

    try:
        conn = http.client.HTTPSConnection(github_api)
        conn.request("GET", endpoint, headers=header)
        response = conn.getresponse()

        if response.status == 403:
            print("Rate Limit Exceeded! Try again later.")
            return
        if response.status != 200:
            print(f"Github API returned status {response.status}")
            return

        data = response.read()
        result = json.loads(data.decode("utf-8"))

    except http.client.HTTPException as e:
        print(f"HTTP error occured: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
    finally:
        conn.close()

    return result

def events(args):
    events = get_data(args)

    limit = args.limit
    if args.commits:
        pushed_commits(args, limit, events)
        return
    
    print(f'Output:')
    repos = pushed_commits(args, limit, events)
    for repo in repos:
        print(f'- Pushed {repos[repo]} to {repo}')
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
    if args.command == 'events':
        args.command = 'starred'
        stars = get_data(args)

        starred = []
        for star in stars:
            starred.append(json.dumps(star['full_name']))

        return starred
    
    else:
        stars = get_data(args)

        if not stars:
            print("No repos have been starred")

        for star in stars:
            print(f'- Starred {json.dumps(star['full_name'])}')

def issues_open(args):
    github_api = "api.github.com"
    endpoint = f"/search/issues?q=author:{args.username}+type:issue+state:open"
    header = {"User-Agent" : "github-cli-fetcher",
              "Accept": "application/vnd.github.v3+json"
              }

    try:
        conn = http.client.HTTPSConnection(github_api)
        conn.request("GET", endpoint, headers=header)

        response = conn.getresponse()

        data = response.read()

        results = json.loads(data.decode("utf-8"))

        items = results.get('items', [])

        if args.command == 'events':
            return items

        if not items:
            print("no open issues")
            return
        else:
            for item in items:
                print(f'- Opened a new issue in {item}')

    except http.client.HTTPException as e:
        print(f"HTTP error occured: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
    finally:
        conn.close()
