import requests

url = "https://api.github.com/search/repositories?q=topic:big-data&sort=stars"
headers = {"Accept": "applicaiton/vnd.github.v3+json"}

r = requests.get(url, headers=headers)
print(f"Status Code: {r.status_code}")

response_dict = r.json()
print(f"Total repos: {response_dict['total_count']}")

repo_dicts = response_dict["items"]
for repo in repo_dicts:
    print(f'repo name: {repo["name"]}')
    print(f'stars: {repo["stargazers_count"]}')
    print(f'language: {repo["language"]}')

    for item in repo["topics"]:
        print(f'topic: {item}')
