import sys
import csv
import json
import subprocess

FILES_PATH = '../crawl-pr/java/files'
REPORT_PATH = '../crawl-pr/report'
REPORT_DIS_OS = '../crawl-pr/report-disable-online-search'
DATA_PATH = '../feedback/csv/data.csv'
valid_urls = list()
deleted_prs = set()
top100repos = None

# 404 Not Found. (deleted by deverlopers)
invalid_urls = ['https://github.com/TNG/ArchUnit/pull/551',
                'https://github.com/meta-abhishek-dawer/GETA2021-Core/pull/13',
                'https://github.com/mak-works/pav-traning/pull/6',
                'https://github.com/gek-m/CalculatorJM/pull/2',
                'https://github.com/MariaNazar/blogPessoal/pull/6',
                'https://github.com/MariaNazar/blogPessoal/pull/4',
                'https://github.com/MariaNazar/blogPessoal/pull/5',
                'https://github.com/gary1998/security-advisor-sdk-java/pull/1',
                'https://github.com/49470488/BilibiliTask/pull/1',
                'https://github.com/49470488/BilibiliTask/pull/2',
                'https://github.com/IDoGeEeeeI/Dz-1/pull/1',
                'https://github.com/gabrilyan88/Java_2/pull/16',
                'https://github.com/Vladimir-Runov/JII_Chat/pull/6',
                'https://github.com/lucile98-ode/GPI-L2BHA-FENOUIL/pull/18']


def get_pr_files_info():
    p = subprocess.Popen(['find', FILES_PATH, '-type', 'f', '-name', 'files.json'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    files_list = [f for f in out.decode().split('\n') if f != '']
    max_file_cnt = 1
    min_file_cnt = sys.maxsize
    max_line_changed = 0
    min_line_changed = sys.maxsize
    max_min_files = [''] * 4
    num_pr_anal = 0
    num_pull_orig = 0
    rows = [['Project', 'Total Files', 'Total Java Files',
             'Max Line Changed in Java Files', 'Min Line Changed in Java Files']]
    rows_unevaluated = [['Project', '# Evaluated PR']]
    proj_unevaluated = dict()
    overlaps_with_top100 = set()
    for f in files_list:
        url = f.replace(FILES_PATH, 'https://github.com').replace('/files.json', '').replace('pulls', 'pull')
        parts = f.replace('../crawl-pr/java/files/', '').split(
            '/')
        proj_name = '/'.join(parts[:2])
        data = json.load(open(f, 'r'))
        java_files = [item for item in data if item['filename'][-5:] == '.java']
        num_pull_orig += 1
        if len(java_files) == 0 or url in invalid_urls:
            if proj_name not in proj_unevaluated:
                proj_unevaluated[proj_name] = 1
            else:
                proj_unevaluated[proj_name] += 1
            continue
        if proj_name in top100repos:
            overlaps_with_top100.add(proj_name)
        num_pr_anal += 1
        file_cnt = len(java_files)
        if max_file_cnt < file_cnt:
            max_file_cnt = file_cnt
            max_min_files[0] = f
        if file_cnt < min_file_cnt:
            min_file_cnt = file_cnt
            max_min_files[1] = f
        cur_max_line_changed, cur_min_line_changed = 0, sys.maxsize
        for item in java_files:
            line_changed = item['changes']
            if max_line_changed < line_changed:
                max_line_changed = line_changed
                max_min_files[2] = f
            if min_line_changed > line_changed:
                min_line_changed = line_changed
                max_min_files[3] = f
            if cur_max_line_changed < line_changed:
                cur_max_line_changed = line_changed
            if cur_min_line_changed > line_changed:
                cur_min_line_changed = line_changed
        rows.append([proj_name, len(data), len(java_files), cur_max_line_changed, cur_min_line_changed])
    print('max_file_cnt', max_file_cnt)
    print('min_file_cnt', min_file_cnt)
    print('max_line_changed', max_line_changed)
    print('min_line_changed', min_line_changed)
    print('max_min_files', max_min_files)
    print('num_pr_anal', num_pr_anal)
    print('num_pull_orig', num_pull_orig)
    print('len(overlaps_with_top100)', len(overlaps_with_top100))
    print('overlaps_with_top100', overlaps_with_top100)
    csv.writer(open('./config/pr_evaluated.csv', 'w')).writerows(rows)
    for key, value in proj_unevaluated.items():
        rows_unevaluated.append([key, value])
    rows_unevaluated.append(['Total', sum(int(row[1]) for row in rows_unevaluated[1:])])
    csv.writer(open('./config/pr_unevaluated.csv', 'w')).writerows(rows_unevaluated)


def merge_pr_diversity_csv():
    table_evaluated = [row for row in csv.reader(open('config/pr_evaluated.csv', 'r'))]
    proj_dict = dict()
    rows = [['Project', '# Evaluated PR', 'Max Total Files', 'Min Total Files', 'Max Total Java Files',
             'Min Total Java Files', 'Max Line Changed in Java Files', 'Min Line Changed in Java Files']]
    for line_no, row in enumerate(table_evaluated):
        if line_no == 0:
            continue
        proj_name = row[0]
        total_files = row[1]
        total_java_files = row[2]
        max_line_changed = row[3]
        min_line_changed = row[4]
        if proj_name not in proj_dict:
            proj_dict[proj_name] = {'evaluated_pr': 1,
                                    'max_total_files': total_files,
                                    'min_total_files': total_files,
                                    'max_total_java_files': total_java_files,
                                    'min_total_java_files': total_java_files,
                                    'max_line_changed': max_line_changed,
                                    'min_line_changed': min_line_changed}
        else:
            proj_dict[proj_name]['evaluated_pr'] += 1
            proj_dict[proj_name]['max_total_files'] = max(proj_dict[proj_name]['max_total_files'], total_files)
            proj_dict[proj_name]['min_total_files'] = min(proj_dict[proj_name]['min_total_files'], total_files)
            if total_java_files != 0:
                # update max_total_java_files, min_total_java_files, max_line_changed, min_line_changed
                proj_dict[proj_name]['max_total_java_files'] = max(proj_dict[proj_name]['max_total_java_files'],
                                                                   total_java_files)
                proj_dict[proj_name]['min_total_java_files'] = min(proj_dict[proj_name]['min_total_java_files'],
                                                                   total_java_files)
                proj_dict[proj_name]['max_line_changed'] = max(proj_dict[proj_name]['max_line_changed'],
                                                               max_line_changed)
                proj_dict[proj_name]['min_line_changed'] = min(proj_dict[proj_name]['min_line_changed'],
                                                               min_line_changed)
    for key, value in proj_dict.items():
        if int(value['max_total_java_files']) > 0:
            rows.append([key, value['evaluated_pr'], value['max_total_files'], value['min_total_files'], value['max_total_java_files'],
                         value['min_total_java_files'], value['max_line_changed'], value['min_line_changed']])

    evaluated_prs = [row[1] for row in rows[1:]]
    max_total_files = [int(row[2]) for row in rows[1:]]
    min_total_files = [int(row[3]) for row in rows[1:]]
    max_total_java_files = [int(row[4]) for row in rows[1:]]
    min_total_java_files = [int(row[5]) for row in rows[1:]]
    max_line_changed_in_java_files = [int(row[6]) for row in rows[1:]]
    min_line_changed_in_java_files = [int(row[7]) for row in rows[1:]]
    rows.append(['Total/Extreme', sum(evaluated_prs), max(max_total_files), min(min_total_files),
    max(max_total_java_files), min(min_total_java_files), max(max_line_changed_in_java_files), min(min_line_changed_in_java_files)])
    csv.writer(open('config/pr_evaluated_merged.csv', 'w')).writerows(rows)


def gen_records_from_report(csv_f, report_path):
    csv_file = open(csv_f, 'w')
    csv_table = [['relative_path', 'html_url', 'path', 'commit_id', 'line', 'bug_type', 'priority']]
    p = subprocess.Popen(['find', report_path, '-type', 'f', '-name', 'report.json'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    files_list = [f for f in out.decode().split('\n') if f != '']
    for f in files_list:
        relative_path = f.replace(report_path + '/', '')
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


def load_top100_libs():
    global top100repos
    top100repos = [line.rstrip().replace('https://github.com/', '') for line in
                   open('../../../top100_mvn_repo.txt', 'r').read().splitlines()][:100]


if __name__ == '__main__':
    load_top100_libs()
    get_pr_files_info()
    merge_pr_diversity_csv()

