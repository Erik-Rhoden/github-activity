import http.client
import json

def foo(args):
    github_api = "api.github.com"
    username = args.username
    endpoint = f"/users/{username}/events"
    header = {"User-Agent" : "github-cli-fetcher"}

    conn = http.client.HTTPSConnection(github_api)
    conn.request("GET", endpoint, headers=header)

    response = conn.getresponse()

    data = response.read()

    events = json.loads(data.decode("utf-8"))

    print(json.dumps(events[0], indent=2))

    conn.close()
