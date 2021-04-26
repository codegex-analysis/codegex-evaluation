import csv
import ast
import json
import random
import subprocess

REPORT_PATH = '../../crawl-pr/report'
REPORT_PATH_WOS = '../../crawl-pr/report_with_online_search'
PROXIES_PATH = './config/proxy_pool.txt'
TOKENS_PATH = './config/tokens.txt'


def gen_records(report_path, record_csv):
    csv_file = open(record_csv, 'w')
    csv_table = [['relative_path', 'html_url', 'path', 'commit_id', 'line', 'bug_type', 'priority', 'comment_or_not',
                  'token', 'proxy']]
    p = subprocess.Popen(['find', report_path, '-type', 'f', '-name', 'report.json'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    files_list = [f for f in out.decode().split('\n') if f != '']
    for f in files_list:
        relative_path = f.replace(report_path+'/', '')
        data = json.load(open(f))
        repo = data['repo']
        pull_number = data['id']
        html_url = "https://github.com/{repo}/pull/{pull_number}/files".format(repo=repo, pull_number=pull_number)
        items = data['items']
        for item in items:
            bug_type = item['type']
            path = item['file_name']
            commit_id = item['commit_sha']
            line = item['line_no']
            priority = item['priority']
            csv_table.append([relative_path, html_url, path, commit_id, line, bug_type, priority, '', '', ''])

    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(csv_table)


def filter_item(record_csv):
    # filter rules (determine whether this comment leave or not)
    csv_reader = csv.reader(open(record_csv, 'r'))
    csv_table = [line for line in csv_reader]
    unique_set = set()
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            continue
        html_url = row[1]
        bug_type = row[5]
        key = ','.join([html_url, bug_type])
        comment_or_not = False
        if key not in unique_set:
            unique_set.add(key)
            comment_or_not = True
        row[7] = str.upper(str(comment_or_not))
    csv.writer(open(record_csv, 'w')).writerows(csv_table)


def apply_token(record_csv):
    tokens_pool = open(TOKENS_PATH, 'r').read().splitlines()
    csv_reader = csv.reader(open(record_csv, 'r'))
    csv_table = [line for line in csv_reader]
    token_dict = dict()
    cur = 0
    unique_set = set()
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            if len(row) == 8:
                csv_table[line_no] = row + ['token']
            continue
        parts = row[1].split('/')
        key = '/'.join([parts[3], parts[4]])
        if key not in token_dict:
            unique_set.add(key)
            token_dict[key] = tokens_pool[cur % len(tokens_pool)]
            cur += 1
        if len(row) == 8:
            csv_table[line_no] = row + [token_dict[key]]
        else:
            row[8] = token_dict[key]
    csv.writer(open(record_csv, 'w')).writerows(csv_table)


def apply_ip(record_csv):
    proxies_pool = [ast.literal_eval(line) for line in open(PROXIES_PATH, 'r').readlines()]
    csv_reader = csv.reader(open(record_csv, 'r'))
    csv_table = [line for line in csv_reader]
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            if len(row) == 9:
                csv_table[line_no] = row + ['proxy']
            continue
        proxy = proxies_pool[random.randint(0, len(proxies_pool) - 1)]
        if len(row) == 9:
            csv_table[line_no] = row + [proxy]
        else:
            row[9] = proxy
    csv.writer(open(record_csv, 'w')).writerows(csv_table)


if __name__ == '__main__':
# generate records step
#     report_paths = [REPORT_PATH, REPORT_PATH_WOS]
#     record_csvs = ['config/record.csv', 'config/record_wos.csv']
#     for i in range(len(report_paths)):
#         gen_records(report_paths[i], record_csvs[i])
#         filter_item(record_csvs[i])
        # apply_token(record_csvs[i])
        # apply_ip(record_csvs[i])
    apply_token('config/new_records.csv')
    apply_ip('config/new_records.csv')




