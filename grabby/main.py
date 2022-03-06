import requests
from datetime import date


def main():

    topic_list = ['big-data']
    url_tuples = map(prepare_github_url, topic_list)

    result_dict = dict()
    for tuple in url_tuples:
        result_dict[tuple[0], get_repo_data(tuple[1])]


def prepare_github_url(topic):
    return topic, f'''https://api.github.com/search/repositories?
               q=topic:{topic}&sort=stars&per_page=100'''


def get_repo_data(repo_url):
    result_dict = dict()
    headers = {"Accept": "applicaiton/vnd.github.v3+json"}

    r = requests.get(repo_url, headers=headers)
    print(f"Status Code: {r.status_code}")

    response_dict = r.json()
    print(f"Total repos: {response_dict['total_count']}")

    repo_dicts = response_dict["items"]
    print(f"Page repos: {len(repo_dicts)}")
    for repo in repo_dicts[:1]:  # first 5 elements for testing
        fill_stats(repo, result_dict)

    return result_dict


def fill_stats(repo, result_dict):
    repo_stats = dict()
    repo_name = repo["name"]
    repo_owner = repo["owner"]["login"]

    repo_stats['date'] = compose_date()
    repo_stats['repo_name'] = repo_name
    repo_stats['owner'] = repo_owner
    repo_stats['star_count'] = repo["stargazers_count"]
    repo_stats['watcher_count'] = repo["watchers_count"]
    repo_stats['fork_count'] = repo["forks_count"]
    repo_stats['topics'] = repo["topics"]
    repo_stats['open_isses'] = repo["open_issues_count"]
    repo_stats['contributors'] = get_count(repo_owner,
                                           repo_name,
                                           'contributors')
    repo_stats['commits'] = get_count(repo_owner,
                                      repo_name,
                                      'commits')
    repo_stats['tags'] = get_count(repo_owner,
                                   repo_name,
                                   'tags')
    repo_stats['closed_issues'] = get_count(repo_owner,
                                            repo_name,
                                            'issues', '&state=closed')

    result_dict[repo_name] = repo_stats


def compose_date():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def get_count(owner, repo_name, suffix, state=''):
    url = prepare_url(owner, repo_name, suffix, state)
    return get_total_count_from_headers(get_headers(url))


def prepare_url(owner, repo_name, suffix, state):
    url = f'''https://api.github.com/repos/
              {owner}/{repo_name}/{suffix}?per_page=1&anon=true{state}'''
    print(f'URL : {url}')
    return url


def get_headers(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.headers

    return dict()


def get_total_count_from_headers(headers: dict):
    pagination_value = headers.get('link')

    if not pagination_value:
        return 0

    print(f'link header value: {pagination_value}')

    last_page_url = pagination_value.split(';')[-2]
    index_page = last_page_url.rfind('page=')
    index_bracket = last_page_url.rfind('>')

    print(f'index_page: {index_page}  | index_bracket: {index_bracket}')

    if index_page < 0 or index_bracket < 0:
        print('count is 0')
        return 0

    count = last_page_url[(index_page + 5):index_bracket]
    print(f'count is {count}')
    return count


if __name__ == "__main__":
    main()
