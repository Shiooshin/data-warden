import requests
from datetime import date
from common.storage.s3_handler import S3Handler
from common.config import Config

import json

__statistics_dict__ = dict()
__repos_dict__ = dict()

__headers__ = {"Accept": "applicaiton/vnd.github.v3+json"}

current_date = date.today().strftime("%Y-%m-%d")

storage_hander = S3Handler()
config = Config()

topic_list = config.get('topic_list')
excluded_repos = config.get('excluded_repo_list')
included_repos = config.get('included_repo_list')
excluded_topics = config.get('excluded_topic_list')
append_repos = config.get('append_repo_list')


def lambda_handler(event, context):

    handle_extra_repos()

    for topic in topic_list:
        __statistics_dict__[topic] = get_repo_data(topic)

    if config.get('debug'):

        json_object = json.dumps(__repos_dict__)
        with open("repos.json", "w") as outfile:
            outfile.write(json_object)

        json_object = json.dumps(__statistics_dict__)
        with open("stats.json", "w") as outfile:
            outfile.write(json_object)

    # storage_hander.write_repository_batch(__repos_dict__)
    # storage_hander.write_statistics_batch(__statistics_dict__)


def handle_extra_repos():
    result_dict = dict()
    extra_repos = get_extra_repos()
    process_repos(extra_repos, result_dict)
    __statistics_dict__['distributed-system'] = result_dict


def get_repo_data(topic):
    result_dict = dict()
    __repo_url__ = f'https://api.github.com/search/repositories?q=topic:{topic}&sort=stars&per_page=100'

    try:
        r = requests.get(__repo_url__, headers=__headers__,
                         auth=(config.get('username', 'github'), config.get('token', 'github')))
    except requests.exceptions.ConnectionError:
        r.status_code = 500

    print(f"Status Code: {r.status_code}")

    if r.status_code != 200:
        print('Request failed')
        return result_dict

    response_dict = r.json()
    print(f"Total repos: {response_dict['total_count']}")

    repo_dicts = response_dict["items"]
    process_repos(repo_dicts, result_dict)
    return result_dict


def process_repos(repo_dicts, result_dict):
    for repo in repo_dicts:
        if repo["stargazers_count"] < config.get('star_limit'):
            break  # no need to go furher, there are only lower star projects

        if not is_valid_repo(repo):
            continue

        if repo["name"] not in excluded_repos:
            fill_stats(repo, result_dict)


def get_extra_repos():
    extra_repos = []

    for append_repo in append_repos:
        repo_url = f'https://api.github.com/search/repositories?q=repo:{append_repo}&sort=stars&per_page=100'

        try:
            r = requests.get(repo_url, headers=__headers__,
                             auth=(config.get('username', 'github'), config.get('token', 'github')))
        except requests.exceptions.ConnectionError:
            print(f'Request failed for url {repo_url}')
            continue

        extra_repos.append(r.json()["items"][0])

    return extra_repos


def is_valid_repo(repo):
    topics = repo["topics"]

    if not topics:
        return False

    if repo["name"] in included_repos:
        return True

    return is_valid_topics(topics)


def is_valid_topics(topics):
    for excluded_topic in excluded_topics:
        if excluded_topic in topics:
            return False
    return True


def fill_stats(repo, result_dict):
    repo_name = repo["name"]
    repo_owner = repo["owner"]["login"]
    repo_tags = repo["topics"]

    if repo_exists(repo_name, repo_owner):
        print(f'repository {repo_name} exists')
        return

    else:
        fill_repo_dict(repo_name, repo_owner, repo_tags)
        repo_stats = fill_repo_stats(repo, repo_name, repo_owner)

    result_dict[repo_name] = repo_stats


def repo_exists(repo_name, repo_owner):
    if repo_name in __repos_dict__:
        return repo_owner == __repos_dict__[repo_name]['owner']

    return False


def get_stats_from_cache(repo_name):
    for value in __statistics_dict__.values():
        if repo_name in value:
            return value[repo_name]


def fill_repo_dict(repo_name, repo_owner, tags):  # TODO add more info for repo dictionary
    __repos_dict__[repo_name] = {'name': repo_name, 'owner': repo_owner, 'tags': tags}


def fill_repo_stats(repo, repo_name, repo_owner):
    repo_stats = dict()
    repo_stats['agg_date'] = current_date
    repo_stats['repo_name'] = repo_name
    repo_stats['owner'] = repo_owner
    repo_stats['star_count'] = repo["stargazers_count"]
    repo_stats['watcher_count'] = repo["watchers_count"]
    repo_stats['fork_count'] = repo["forks_count"]
    repo_stats['topics'] = repo["topics"]
    repo_stats['open_issues'] = repo["open_issues_count"]
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
    return repo_stats


def get_count(owner, repo_name, suffix, state=''):
    url = prepare_url(owner, repo_name, suffix, state)
    return get_total_count_from_headers(get_headers(url))


def prepare_url(owner, repo_name, suffix, state):
    url = f'https://api.github.com/repos/{owner}/{repo_name}/{suffix}?per_page=1&anon=true{state}'
    return url


def get_headers(url):
    response = requests.get(url, auth=(config.get('username', 'github'), config.get('token', 'github')))

    if response.status_code == 200:
        print(f"requests left: {response.headers.get('x-ratelimit-remaining')}")  # TODO if limit < 0 wait
        return response.headers

    return dict()


def get_total_count_from_headers(headers: dict):
    pagination_value = headers.get('link')

    if not pagination_value:
        return 0

    last_page_url = pagination_value.split(';')[-2]
    index_page = last_page_url.rfind('page=')
    index_bracket = last_page_url.rfind('>')

    if index_page < 0 or index_bracket < 0:
        print('count is 0')
        return 0

    count = last_page_url[(index_page + 5):index_bracket]
    return count


# if __name__ == "__main__":
#     lambda_handler(None, None)
