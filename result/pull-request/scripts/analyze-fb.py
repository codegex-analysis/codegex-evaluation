import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
DATA_PATH = '../feedback/csv/data.csv'

AF = 'Accept and fix'
AC = 'Accept'
NI = 'Not interested'
FP = 'Marked as fp'
MR = 'Marked as resolved but did not reply'
pattern_dict = dict()


def load_pattern_dict():
    global pattern_dict
    csv_table = [row for row in csv.reader(open(DATA_PATH, 'r'))]
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            continue
        else:

            note = row[7]
            if 'delete' in note:
                continue
            feedback = row[8]
            if '404 Not Found' in feedback:
                continue
            pattern = row[4]
            if any(key == feedback for key in (AF, AC, NI, FP, MR)) and pattern not in pattern_dict:
                pattern_dict[pattern] = {'AF': 0, 'AC': 0, 'NI': 0, 'FP': 0, 'MR': 0}
            if feedback == AF:
                pattern_dict[pattern]['AF'] += 1
            elif feedback == AC:
                pattern_dict[pattern]['AC'] += 1
            elif feedback == NI:
                pattern_dict[pattern]['NI'] += 1
            elif feedback == FP:
                pattern_dict[pattern]['FP'] += 1
            elif feedback == MR:
                pattern_dict[pattern]['MR'] += 1
    pattern_dict = sorted(pattern_dict.items(), key=lambda x: (x[1]['AF'] + x[1]['AC'] + x[1]['NI'] + x[1]['FP'] + x[1]['MR']))
    sums = [['AF', 'AC', 'NI', 'MR', 'FP'], [0]*5]
    for pattern in pattern_dict:
        sums[1] = [sums[1][0] + pattern[1]['AF'], sums[1][1] + pattern[1]['AC'], sums[1][2] + pattern[1]['NI'], 
        sums[1][3] + pattern[1]['MR'], sums[1][4] + pattern[1]['FP']]
    print('total_feedback', str(sum(sums[1])))
    print('AF+AC', str((sums[1][0] + sums[1][1])))
    print('(AF+AC) / total', str(round((sums[1][0] + sums[1][1]) * 100/sum(sums[1]), 2)))
    print(sums[0])
    print(sums[1])

def draw_staked_bar():
    load_pattern_dict()
    patterns = [''] * len(pattern_dict)
    FPs = [0] * len(patterns)
    NIs = [0] * len(patterns)
    MRs = [0] * len(patterns)
    ACs = [0] * len(patterns)
    AFs = [0] * len(patterns)
    for idx, content in enumerate(pattern_dict):
        patterns[idx] = content[0]
        AFs[idx] = content[1]['AF']
        ACs[idx] = content[1]['AC']
        NIs[idx] = content[1]['NI']
        FPs[idx] = content[1]['FP']
        MRs[idx] = content[1]['MR']
    print('patterns', patterns)
    print('FPs', FPs, str(sum(FPs)))
    print('NIs', NIs, str(sum(NIs)))
    print('MRs', MRs, str(sum(MRs)))
    print('ACs', ACs, str(sum(ACs)))
    print('AFs', AFs, str(sum(AFs)))
    bar_height = 0.8

    print('len patterns', len(patterns))
    plt.barh(patterns, FPs, color='black', alpha=1, edgecolor="k", height=bar_height)
    plt.barh(patterns, NIs, hatch='|||||', color='white', alpha=1, edgecolor="k", left=FPs, height=bar_height)
    plt.barh(patterns, MRs, hatch='----', color='white', alpha=1, edgecolor="k",
             left=[FPs[i] + NIs[i] for i in range(len(patterns))], height=bar_height)
    plt.barh(patterns, ACs, hatch='/////', color='white', alpha=1, edgecolor="k",
             left=[FPs[i] + NIs[i] + MRs[i] for i in range(len(patterns))], height=bar_height)
    plt.barh(patterns, AFs, color='white', alpha=1, edgecolor="k",
             left=[FPs[i] + NIs[i] + MRs[i] + ACs[i] for i in range(len(patterns))], height=bar_height)
    xc = [x * 5 for x in range(int(max([FPs[i] + NIs[i] + MRs[i] + ACs[i] + AFs[i] for i in range(len(patterns))]) / 5) + 1)]
    plt.xticks(xc, fontsize=13)
    plt.yticks(fontsize=13)
    plt.tight_layout()
    labels = ['FP', 'NI', 'MR', 'AC', 'AF']
    plt.legend(labels, loc='center right', bbox_to_anchor=(0.5, 0., 0.5, 0.5), frameon=False,
                        fontsize='xx-large')
    for x in xc:
        plt.axvline(x=x, color='black', linewidth='0.4')
    # top value
    for i, v in enumerate([FPs[i] + NIs[i] + MRs[i] + ACs[i] + AFs[i] for i in range(len(patterns))]):
        plt.text(v, i, " " + str(v), color='black', va='center')
    plt.show()


def parse_url(html_url):
    tokens = html_url.split('/')
    owner = tokens[3]
    repo = tokens[4]
    pull_number = tokens[6]
    return owner, repo, pull_number


def cnt_total_pr_comment():
    csv_table = [row for row in csv.reader(open(DATA_PATH, 'r'))]
    total_pr_comment = set()
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            continue
        else:
            html_url = row[0]
            note = row[7]
            if any(key in note for key in ('delete', '404 Not Found')):
                continue
            owner, repo, pull_number = parse_url(html_url)
            key = ','.join([owner, repo, pull_number])
            if key not in total_pr_comment:
                total_pr_comment.add(key)
    print('total_pr_comment', len(total_pr_comment))


if __name__ == '__main__':
    cnt_total_pr_comment()
    draw_staked_bar()
