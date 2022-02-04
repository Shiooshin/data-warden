import requests

url = "https://api.github.com/search/repositories?q=topic:big-data&sort=stars&per_page=100"
headers = {"Accept": "applicaiton/vnd.github.v3+json"}

r = requests.get(url, headers=headers)
print(f"Status Code: {r.status_code}")

response_dict = r.json()
print(f"Total repos: {response_dict['total_count']}")

repo_dicts = response_dict["items"]
print(f"Page repos: {len(repo_dicts)}")
for repo in repo_dicts[:5]:  # first 5 elements for testing
    print(f'repo name: {repo["name"]}')
    print(f'stars: {repo["stargazers_count"]}')
    print(f'watches: {repo["watchers_count"]}')
    print(f'open_issues_count: {repo["open_issues_count"]}')
    print(f'topics: {repo["topics"]}')
    print(f'forks_count: {repo["forks_count"]}')
