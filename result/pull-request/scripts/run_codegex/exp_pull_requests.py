import glob
import re
from os import path
import json

from patterns.models.context import Context
from patterns.models.engine import DefaultEngine
from rparser import parse
from utils import create_missing_dirs
from timer import Timer
from gen_detectors import DETECTOR_DICT

root = 'PullRequests/java/files'
report_path = 'PullRequests/report'
create_missing_dirs(report_path)

RE_SHA = re.compile(r'https://github\.com/[^/]+/[^/]+/blob/(\w+)/')


def _get_sha(blob_url: str):
    try:
        m = RE_SHA.search(blob_url)
        if m:
            return m.groups()[0]

    except TypeError as e:
        # "blob_url": null
        return ''


def report_diversity():
    paths = glob.glob(f'{report_path}/**/report.json', recursive=True)
    diversity = dict()

    for p in paths:
        with open(p, 'r') as file_to_read:
            file_json = json.load(file_to_read)
            items = file_json['items'] if 'items' in file_json else list()
            for bug_instance in items:
                pattern_name = bug_instance['type']
                if pattern_name in diversity:
                    diversity[pattern_name] += 1
                else:
                    diversity[pattern_name] = 1

    with open(f'{report_path}/diversity.json', 'w') as outfile:
        json.dump(diversity, outfile)


def sum_time_and_warnings():
    with open(f'{report_path}/diversity.json', 'r') as f:
        jfile = json.load(f)
        sum = 0
        for k, v in jfile.items():
            sum += v
        print(f'sum of diversity = {sum}')

    with open(f'{report_path}/time_projects.json', 'r') as f:
        jfile = json.load(f)
        sum = 0
        for k, v in jfile.items():
            sum += v
        print(f'sum of time = {sum}')


def get_modified_patchset(path):
    patchset = []
    with open(path, 'r') as jf:
        jfile = json.load(jf)
        for file in jfile:
            name = file['filename']

            if name.endswith('.java'):
                if 'patch' in file and file['status'] != 'removed':
                    patch = parse(file['patch'], name=name)
                    patch.type = file['status']
                    if 'blob_url' in file:
                        patch.sha = _get_sha(file['blob_url'])
                    patchset.append(patch)
    return patchset


def run():
    paths = glob.glob(f'{root}/**/files.json', recursive=True)

    context = Context()
    # context.enable_online_search()
    engine = DefaultEngine(context)

    re_repo = re.compile(r'PullRequests/java/files/(.+?)/pulls/(\d+)')

    for p in paths:
        m = re_repo.search(p)
        if m:
            repo_name = m.groups()[0]
            pr_id = m.groups()[1]
            engine.context.update_repo_name(repo_name)
        else:
            continue

        patchset = get_modified_patchset(p)
        if patchset:
            pr_timer = Timer(repo_name + '-' + pr_id, logger=None)
            pr_timer.start()
            engine.visit(*patchset)

            bugs = engine.filter_bugs()
            if bugs:
                save_path = f'{report_path}/{repo_name}/{pr_id}'
                create_missing_dirs(save_path)
                with open(f'{save_path}/report.json', 'w') as out:
                    bugs_json = dict()
                    bugs_json['repo'] = repo_name
                    bugs_json['id'] = pr_id
                    bugs_json['total'] = len(bugs)
                    bugs_json['items'] = [bug.__dict__ for bug in bugs]
                    json.dump(bugs_json, out)
            pr_timer.stop()

    project_time_dict = dict()
    detector_time_dict = dict()
    for k, v in Timer.timers.items():
        if k not in DETECTOR_DICT:
            project_time_dict[k] = v
        else:
            detector_time_dict[k] = v
    with open(path.join(report_path, 'time_projects.json'), 'w') as logfile:
        json.dump(project_time_dict, logfile)
    with open(path.join(report_path, 'time_detectors.json'), 'w') as logfile:
        json.dump(detector_time_dict, logfile)


if __name__ == '__main__':
    run()
    report_diversity()
    sum_time_and_warnings()
