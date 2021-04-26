import os
import csv

csv_base_path = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/csv'
def analyze_rbugs_report():
    proj_list = [os.path.join(csv_base_path, proj) for proj in os.listdir(csv_base_path)
                 if os.path.isdir(os.path.join(csv_base_path, proj))]
    pattern_dict = dict()
    spotbugs_diff_csv = os.path.join(csv_base_path, 'spotbugs_diff.csv')
    spotbugs_diff_table = []
    for proj in proj_list:
        spotbugs = os.path.join(proj, 'spotbugs.csv')
        spotbugs_ = os.path.join(proj, 'spotbugs_.csv')
        if os.path.exists(spotbugs_):
            spotbugs__csv = [row for row in csv.reader(open(spotbugs_, 'r'))]
            if os.path.exists(spotbugs):
                spotbugs_csv = [row for row in csv.reader(open(spotbugs, 'r'))]
            else:
                spotbugs_csv = []
            spotbugs_diff_table += [[proj] + row for row in spotbugs__csv if row not in spotbugs_csv]
    csv.writer(open(spotbugs_diff_csv, 'w')).writerows(spotbugs_diff_table)

if __name__ == '__main__':
    analyze_rbugs_report()
