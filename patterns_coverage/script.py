import re
import json
import os
import requests

# Paths
SP_HTML = 'resources/spotbugs.html'
SP_PATTERNS = 'out/spotbugs_patterns.json'
SP_SUMMARY = 'out/spotbugs_summary.json'

RES_CD_PATTERNS = 'resources/Codegex_patterns_short.txt'
CG_PATTERNS = 'out/codegex_patterns.json'
CG_SUMMARY = 'out/codegex_summary.json'

COVERAGE = 'out/coverage.json'

RES_TAB_NAMES = 'resources/tab_names.txt'
TAB_NAMES = 'out/tab_names.txt'
TAB_IMPLEMENT = 'out/tab_implement.txt'


# ===============  SpotBugs ===============
def download_SP_html():
    if os.path.exists(SP_HTML):
        return
    link = 'https://spotbugs.readthedocs.io/en/stable/bugDescriptions.html'
    res = requests.get(link, stream=False, timeout=10)
    res.encoding = 'utf-8'
    if res.status_code == 200 or res.status_code == 304:
        os.makedirs('html', exist_ok=True)
        with open(SP_HTML, 'w') as out:
            out.write(res.text)


def parse_SP_html():
    """
    Categorize spotbugs patterns, and write it to SP_PATTERNS
    """
    re_header = re.compile(r'<h2>(.+?)<a\s+class=\"headerlink\"')
    re_pattern = re.compile(r'<h3>(.+?)<a\s+class=\"headerlink\"\s+href=\"#')
    category_dict = dict()
    with open(SP_HTML, 'r') as f:
        category = None
        for line in f:
            m = re_header.search(line)
            if m:
                category = m.group(1)
                category_dict[category] = list()
            else:
                m = re_pattern.search(line)
                if m:
                    pattern = m.group(1)
                    if '&amp;' in pattern:
                        pattern = pattern.replace('&amp;', '&')
                    if '&#64;' in pattern:
                        pattern = pattern.replace('&#64;', '@')
                    assert category
                    category_dict[category].append(pattern)

    os.makedirs('out', exist_ok=True)
    with open(SP_PATTERNS, 'w') as out:
        json.dump(category_dict, out)

    # Summary
    summary = dict()
    sum = 0
    categories = dict()
    for k, v in category_dict.items():
        sum += len(v)
        categories[k] = len(v)
    summary['categories'] = categories
    summary['sum'] = sum

    with open(SP_SUMMARY, 'w') as out:
        json.dump(summary, out)


# ===============  Codegex ===============
def categorize_CD():
    """
    Categorize Codegex patterns according to short names in RES_CD_PATTERNS, write it to CG_PATTERNS
    """

    def _add_to_list(key, dic: dict, elem):
        val = dic.get(key, list())
        val.append(elem)
        dic[key] = val

    # Read resource
    with open(RES_CD_PATTERNS, 'r') as f:
        rbugs_pattern_set = set([line.strip() for line in f])
    # Load spotbugs pattern
    with open(SP_PATTERNS, 'r') as f:
        spotbugs_dict = json.load(f)
    # Categorize
    category_dict = dict()
    for p1 in rbugs_pattern_set:
        has_found = False
        for category, pattern_list in spotbugs_dict.items():
            for p2 in pattern_list:
                if p1 in p2:
                    _add_to_list(category, category_dict, p2)
                    has_found = True
                    break
            if has_found:
                break
        if not has_found:
            print(f'[Not Found]{p1}')

    os.makedirs('out', exist_ok=True)
    with open(CG_PATTERNS, 'w') as out:
        json.dump(category_dict, out)

    # Summary
    summary = dict()
    sum = 0
    categories = dict()
    for k, v in category_dict.items():
        sum += len(v)
        categories[k] = len(v)
    summary['categories'] = categories
    summary['sum'] = sum

    with open(CG_SUMMARY, 'w') as out:
        json.dump(summary, out)


def compute_coverage():
    """
    Compute the ratio of Codegex patterns against SpotBugs patterns, and write it to COVERAGE 
    """
    # Load dicts
    with open(SP_PATTERNS, 'r') as f:
        SP_dict = json.load(f)
    with open(CG_PATTERNS, 'r') as f:
        CG_dict = json.load(f)

    # Compute
    coverage_dict = dict()
    for k, v in CG_dict.items():
        if k in SP_dict and len(SP_dict[k]) != 0:
            percentage = len(v) / len(SP_dict[k]) * 100
            coverage_dict[k] = format(percentage, '0.2f') + '%'

    with open(COVERAGE, 'w') as out:
        json.dump(coverage_dict, out)


# ===============  Study table ===============
def complete_pattern_names():
    """
    Complete pattern names in the study table according to SP_PATTERNS, and write it to TAB_NAMES
    """
    with open(RES_TAB_NAMES, 'r') as f:
        res_tab_names = [line.strip() for line in f]

    with open(SP_PATTERNS, 'r') as f:
        SP_dict = json.load(f)

    SP_set = set()
    for k, v in SP_dict.items():
        SP_set.update(v)

    # match
    complete_names = list()
    for name in res_tab_names:
        to_search = name if name.endswith(')') else f'{name} ('
        to_del = None

        hit = False
        for long_name in SP_set:
            if long_name.startswith(to_search):
                complete_names.append(long_name)
                hit = True
                break

        if to_del:
            SP_set.remove(to_del)

        if not hit:
            print(f'[Fail to Complete] {name}')
            complete_names.append(name)

    with open(TAB_NAMES, 'w') as out:
        out.write('\n'.join(complete_names))


def mark_implemented():
    """
    Write 'Y' or 'N' for each patterns in TAB_NAMES to TAB_IMPLEMENT
    """
    with open(CG_PATTERNS, 'r') as f:
        CG_dict = json.load(f)

    CG_set = set()
    for k, v in CG_dict.items():
        CG_set.update(v)

    with open(TAB_NAMES, 'r') as f:
        tab_names = [line.strip() for line in f]

    marks = list()
    for name in tab_names:
        if name in CG_set:
            marks.append('Y')
        else:
            marks.append('N')

    with open(TAB_IMPLEMENT, 'w') as out:
        out.write('\n'.join(marks))



if __name__ == '__main__':
    # download_SP_html()
    # parse_SP_html()
    # categorize_CD()
    # compute_coverage()
    # complete_pattern_names()
    mark_implemented()
