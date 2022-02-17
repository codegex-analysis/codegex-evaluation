"""
TODO: write csv by csv module
Filter bug instances of new implemented patterns
"""
#%%
import re
from pathlib import Path
import os
import json

path_cur = Path(__file__).resolve().parent
path_report =  path_cur / "log" / "report"

def get_pattern_abbr():
    re_abbr = re.compile(r'\(([A-Z\d]+(?:_[A-Z\d]+)+)\)')
    
    with open(path_cur / "new_patterns.txt", 'r') as f:
        content = f.read()

    patterns = re_abbr.findall(content)
    with open('new_pattern_abbr.json', 'w') as out:
        json.dump(patterns, out)
    return set(patterns)


def filter():
    pattern_abbr = get_pattern_abbr()

    path_incremental_report = path_cur / "log" / "incremental_report"

    repo_names = next(os.walk(path_report))[1]  # (dirpath, dirnames, filenames), only want dirnames

    pattern_summary = dict()
    csv_lines = list()

    for name in repo_names:
        path_json = path_report / name / "bug_instances.json"
        with open(path_json, 'r') as f:
            bug_ins = json.load(f)

        new_bug_ins = {'repo': name, 'total': 0, 'items': list()}
        csv_per_repo = list()
        for ins in bug_ins['items']:
            pattern_type = ins['type']
            if pattern_type in pattern_abbr:
                new_bug_ins['items'].append(ins)
                csv_lines.append(f"{name},{pattern_type},{ins['file_name']},{ins['line_no']},{ins['line_content']}\n")
                csv_per_repo.append(f"{pattern_type},{ins['file_name']},{ins['line_no']},{ins['line_content']}\n")
                # update pattern summary
                if pattern_type in pattern_summary:
                    pattern_summary[pattern_type] += 1
                else:
                    pattern_summary[pattern_type] = 1

        new_bug_ins['total'] = len(new_bug_ins['items'])
                

        # write files
        if new_bug_ins['total'] > 0:
            path_repo = path_incremental_report / name
            os.makedirs(path_repo, exist_ok=True)

            with open(path_repo / "bug_instances.json", 'w') as out:
                json.dump(new_bug_ins, out)

            with open(path_repo / "rbugs.csv", 'w') as out:
                out.writelines(csv_per_repo)

    with open(path_incremental_report / "instances.csv", 'w') as out:
        out.writelines(csv_lines)

    with open(path_incremental_report / 'pattern_summary.json', 'w') as out:
        json.dump(pattern_summary, out)

filter()