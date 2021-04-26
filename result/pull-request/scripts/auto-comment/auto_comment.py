import json
import os
import sys
import csv
import time
import ast
import random
import requests
sys.path.append(os.path.dirname(__file__))
import util


PATTERN_DICT_PATH = './config/pattern_dict.json'
RECORDS_PATH = './config/new_records.csv'
PROXIES_PATH = './config/proxy_pool.txt'

pattern_dict = None


def create_comment(owner: str, repo: str, pull_number: int, body: str, commit_id: str, path: str, line: int, token: str,
                   proxies: dict):
    query_url = "https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments".format(owner=owner,
                                                                                                  repo=repo,
                                                                                                  pull_number=
                                                                                                  pull_number)
    comment_url = "https://github.com/{owner}/{repo}/pull/{pull_number}".format(owner=owner,
                                                                                repo=repo,
                                                                                pull_number=pull_number)
    params = {
        "body": body,
        "commit_id": commit_id,
        "path": path,
        "side": "RIGHT",
        "line": line,
    }
    headers = {'Authorization': f'token {token}', 'accept': "application/vnd.github.v3+json"}
    # print(query_url)
    r = util.post_requests(query_url, params, headers, proxies)
    if r.status_code == 201:
        print('link:', comment_url)
        return comment_url
    else:
        print("status_code", r.status_code, 'link', comment_url, 'content', r.content)
    print('link:', comment_url)


def get_proxy():
    proxies_pool = [ast.literal_eval(line) for line in open(PROXIES_PATH, 'r').readlines()]
    check_urllist = ['http://www.baidu.com', 'http://www.taobao.com', 'https://cloud.tencent.com/']
    while True:
        proxy = proxies_pool[random.randint(0, len(proxies_pool) - 1)]
        try:
            response = requests.get(random.choice(check_urllist), proxies=proxy, timeout=1)
            if response.status_code:
                return proxy
        except Exception as e:
            continue


def load_pattern_dict():
    global pattern_dict
    pattern_dict = json.load(open(PATTERN_DICT_PATH, 'r'))


def get_body(pattern_name):
    category_name = pattern_dict[pattern_name]['category_name']
    category_href = pattern_dict[pattern_name]['category_href']
    des_title = pattern_dict[pattern_name]['des_title']
    des_detail = pattern_dict[pattern_name]['des_detail']
    pattern_href = pattern_dict[pattern_name]['pattern_href']
    body = '''I detect that this code is problematic. According to the [{category_name}]\
({category_href}), [{des_title}]({pattern_href}).
{des_detail}'''.format(category_name=category_name,
                       category_href=category_href,
                       des_title=des_title,
                       des_detail=des_detail,
                       pattern_href=pattern_href)
    return body


def read_csv():
    csv_table = [line for line in csv.reader(open(RECORDS_PATH, 'r'))]
    comments_info = []
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            continue
        comment = dict()
        html_url = row[1]
        owner, repo, pull_number = parse_html(html_url)
        path = row[2]
        commit_id = row[3]
        line = row[4]
        bug_type = row[5]
        comment_or_not = row[7]
        token = row[8]
        state = row[10]
        if comment_or_not == 'TRUE' and state == 'open':
            body = get_body(bug_type)
            comment["owner"] = owner
            comment["repo"] = repo
            comment["pull_number"] = pull_number
            comment["commit_id"] = commit_id
            comment["path"] = path
            comment["line"] = int(line)
            comment["type"] = bug_type
            comment["body"] = body
            comment['token'] = token
            comments_info.append(comment)
    return comments_info


def parse_html(url):
    tokens = url.split('/')
    owner = tokens[3]
    repo = tokens[4]
    pull_number = tokens[6]
    return owner, repo, pull_number


def get_pr_status(owner: str, repo: str, pull_number: int, token: str):
    query_url = "https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}".format(owner=owner,
                                                                                                  repo=repo,
                                                                                                  pull_number=
                                                                                                  pull_number)
    headers = {'Authorization': f'token {token}', 'accept': "application/vnd.github.v3+json"}
    comment_url = "https://github.com/{owner}/{repo}/pull/{pull_number}".format(owner=owner,
                                                                                repo=repo,
                                                                                pull_number=pull_number)
    # print(query_url)
    r = util.get_requests(query_url, headers)
    if r.status_code == 200:
        print(comment_url, r.json()['state'])
    else:
        print(comment_url, 'error')


def create_comment_from_comments_info(comments_info):
    for comment in comments_info:
        # owner: str, repo: str, pull_number: int, body: str, commit_id: str, path: str, line: int

        create_comment(comment['owner'], comment['repo'], comment['pull_number'], comment['body'],
                       comment['commit_id'], comment['path'], comment['line'], comment['token'],
                       get_proxy())
        # get_pr_status(comment['owner'], comment['repo'], comment['pull_number'], comment['token'])
        print('time sleep for 60s.')
        time.sleep(60)


if __name__ == '__main__':
    load_pattern_dict()
    comments_info = read_csv()
    print('start auto-commenting for {} items.'.format(str(len(comments_info))))
    create_comment_from_comments_info(comments_info)
