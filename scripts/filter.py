import os
import csv
from subprocess import Popen, PIPE

csv_base_path = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/csv'
max_diff = 5
csv_content_dict = None

def analyze_rbugs_report():
    # csv_f = csv.writer(open('rbugs_fp_check_2.csv', 'w'))
    csv_f_table = [['proj_name', 'bug_pattern', 'file_path', 'line']]
    proj_list = [os.path.join(csv_base_path, proj) for proj in os.listdir(csv_base_path)
                 if os.path.isdir(os.path.join(csv_base_path, proj))]
    pattern_dict = dict()
    for proj in proj_list:
        spotbugs_report_path = os.path.join(proj, 'spotbugs.csv')
        rbugs_report_path = os.path.join(proj, '{}.csv'.format(proj))
        if os.path.exists(spotbugs_report_path):
            continue
        if not os.path.exists(rbugs_report_path):
            rbugs_csv = []
            print(rbugs_report_path, 'Not Exist!')
        else:
            rbugs_csv = [row for row in csv.reader(open(rbugs_report_path, 'r'))]
        
        for row in rbugs_csv:
            pattern = row[0]
            path = row[1]
            line = row[2]
            csv_f_table.append([os.path.basename(proj), pattern, path, line])
    # csv_f.writerows(csv_f_table)
    # sortedDict = dict(sorted(pattern_dict.items(), key=lambda item: item[1], reverse=True))
    # total = 0
    # for key, value in sortedDict.items():
    #     total += value
    #     print(key, value)
    # print('total bugs number:', total)

def match():
    global csv_content_dict
    proj_list = [os.path.join(csv_base_path, proj) for proj in os.listdir(csv_base_path)
                        if os.path.isdir(os.path.join(csv_base_path,proj))]
    matched_dict = dict()
    csv_content_dict = dict()
    rbugs_lines = 0
    for proj in proj_list:
        spotbugs_report_path = os.path.join(proj, 'spotbugs.csv')
        rbugs_report_path = os.path.join(proj, 'rbugs.csv')
        if not os.path.exists(spotbugs_report_path):
            print(proj, "SpotBugs csv does not exist.")
            continue

        # construct spotbugs_analyzed_java_files
        spotbugs_analyzed_java_files = set()
        spotbugs_csv = [row for row in csv.reader(open(spotbugs_report_path, 'r'))]
        rbugs_csv = []
        if os.path.exists(rbugs_report_path):
            rbugs_csv = [row for row in csv.reader(open(rbugs_report_path, 'r'))]
        else:
            print(proj, "RBugs csv does not exist.")
        rbugs_lines += len(rbugs_csv)
        csv_content_dict[os.path.basename(proj)] = {'spotbugs_csv': spotbugs_csv, 'rbugs_csv': rbugs_csv}

        for row in spotbugs_csv:
            path = row[2]
            spotbugs_analyzed_java_files.add(path)


    #     # -1 means not match, otherwise represents the row number in spotbugs csv file
        spotbugs_matched_table = [-1] * len(spotbugs_csv)
        rbugs_matched_table = [-1] * len(rbugs_csv)

    #     # print(spotbugs_row_count, rbugs_row_count)
        for idx_1, row_1 in enumerate(rbugs_csv):
            bug_pattern_1 = row_1[0]
            path_1 = row_1[1]
            line_1 = row_1[2]
            # check whether path in spotbugs analyzed java files
            is_valid = False
            for file in spotbugs_analyzed_java_files:
                if file in path:
                    is_valid = True
                    break

            if not is_valid:
                rbugs_matched_table[idx_1] = -2
                continue

    #         # match if is_valid
            min_off = max_diff + 1
            min_row = None

            for idx_2, row_2 in enumerate(spotbugs_csv):
                if spotbugs_matched_table[idx_2] == -1:
    #                 # bug pattern of spotbugs is not matched
                    bug_pattern_2 = row_2[0]
                    path_2 = row_2[1]
                    line_2 = row_2[2]
                    if bug_pattern_1 == bug_pattern_2 and path_2 in path_1:
                        off = abs(int(line_1) - int(line_2))
                        if off < min_off and off < max_diff:
                            min_row = idx_2
            if min_row is not None:
                spotbugs_matched_table[min_row] = idx_1
                rbugs_matched_table[idx_1] = min_row
        # print('[Porject Name]:', os.path.basename(proj))
        # print('[SpotBugs Matched Table]')
        # print(str(spotbugs_matched_table))
        # print('[RBugs Matched Table]')
        # print(str(rbugs_matched_table))
        matched_dict[os.path.basename(proj)] = {'st': spotbugs_matched_table, 'rt': rbugs_matched_table}
    return matched_dict

def get_result(matched_dict: dict):
    # csv_f = csv.writer(open('rbugs_fp_check_1.csv', 'w'))
    csv_f_table = [['proj_name', 'bug_pattern', 'file_path', 'line']]
    total_matched = 0
    total_spotbugs_left = 0
    total_rbugs_left = 0
    pattern_dict = dict()
    for key, value in matched_dict.items():
        st = value["st"]
        rt = value["rt"]
        matched = len([n for n in st if n != -1])
        spotbugs_left = len(st) - matched
        rbugs_left = len(rt) - matched - len([n for n in rt if n == -2])
        # ?? no invalid item
        # print('invalid rbugs items(detect files ...):', len([n for n in rt if n == -2]))
        total_matched += matched
        total_spotbugs_left += spotbugs_left
        total_rbugs_left += rbugs_left

        # spotbugs_csv = csv_content_dict[key]['spotbugs_csv']
        rbugs_csv = csv_content_dict[key]['rbugs_csv']
        rows = [i for i in range(len(rt)) if rt[i] == -1]
        for row in rows:
            csv_f_table.append([key, rbugs_csv[row][0], rbugs_csv[row][1], rbugs_csv[row][2]])
            pattern = rbugs_csv[row][0]
            if pattern not in pattern_dict:
                pattern_dict[pattern] = 1
            else:
                pattern_dict[pattern] += 1
    print("csv_table len", len(csv_f_table))
    # csv_f.writerows(csv_f_table)
    print('total_matched', total_matched)
    print('total_spotbugs_left', total_spotbugs_left)
    print('total_rbugs_left', total_rbugs_left)
    # sortedDict = dict(sorted(pattern_dict.items(), key=lambda item: item[1], reverse=True))
    # for key, value in sortedDict.items():
    #     print(key, value)

def write_rbugs_execute_result():
    execute_csv_path = '/home/codegex/Documents/workspace/rbugs/experiment/log/execute/execute-result.csv'
    csv_table = [row for row in csv.reader(open(execute_csv_path, 'r'))]
    rbugs_time_log = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/rbugs/time.log'
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            csv_table[line_no] = row + ['rbugs execute time']
        else:
            out, err = Popen('grep -h \'^{}\\s\' {} | tr -s \' \' | cut -d \' \' -f 2'.format(row[0], rbugs_time_log), stdout=PIPE, stderr=PIPE, shell=True).communicate()
            time = out.decode().strip()
            if time == '':
                csv_table[line_no] = row + ['-']
            else:
                csv_table[line_no] = row + ['{} s'.format(time)]
    result_log = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/comparison-result.csv'
    csv_writer = csv.writer(open(result_log, 'w'))
    csv_writer.writerows(csv_table)


def write_speed_up():
    result_log = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/comparison-result.csv'
    csv_table = [row for row in csv.reader(open(result_log, 'r'))]
    new_table = []
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            new_table.append(row + ['speedup with compilation time', 'speedup with compilation time(np)', 'speedup without compilation time'])
        else:
            if row[1] == 'SUCCESS' and row[4] == 'SUCCESS':
                compile_time = convert_time(row[2])
                compile_time_np = convert_time(row[3])
                spotbugs_execute_time = convert_time(row[5])
                rbugs_execute_time = convert_time(row[6])
                speedup_with_compile = round((spotbugs_execute_time+compile_time)/rbugs_execute_time)
                speedup_with_compile_np = round((spotbugs_execute_time+compile_time_np)/rbugs_execute_time)
                speedup_without_compile = round(spotbugs_execute_time/rbugs_execute_time)
                # print(str(speedup_with_compile), str(speedup_without_compile))
                new_table.append(row + [speedup_with_compile, speedup_with_compile_np, speedup_without_compile])
    new_result_log = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/comparison-result-speedup.csv'
    csv_writer = csv.writer(open(new_result_log, 'w'))
    csv_writer.writerows(new_table)


def write_match_result(matched_dict: dict):
    matched_csv = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/matched-result.csv'
    spotbugs_unmatched_csv = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/spotbugs-unmatched-result.csv'
    rbugs_unmatched_csv = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/rbugs-unmatched-result.csv'
    matched_table = [['project name', 'pattern', 'spotbugs path', 'spotbugs lineno', 'rbugs path', 'rbugs lineno']]
    spotbugs_unmatched_table = []
    rbugs_unmatched_table = []
    for key, value in matched_dict.items():
        st = value["st"]
        rt = value["rt"]
        for i, j in enumerate(st):
            if j == -1:
                spotbugs_unmatched_table.append([key] + csv_content_dict[key]['spotbugs_csv'][i])
            elif j > -1:
                matched_table.append([key] + csv_content_dict[key]['spotbugs_csv'][i] + csv_content_dict[key]['rbugs_csv'][j][1:3])
        for i, j in enumerate(rt):
            if j == -1:
                rbugs_unmatched_table.append([key] + csv_content_dict[key]['rbugs_csv'][i])
    matched_csv_writer = csv.writer(open(matched_csv, 'w'))
    spotbugs_unmatched_csv_writer = csv.writer(open(spotbugs_unmatched_csv, 'w'))
    rbugs_unmatched_csv_writer = csv.writer(open(rbugs_unmatched_csv, 'w'))
    matched_csv_writer.writerows(matched_table)
    spotbugs_unmatched_csv_writer.writerows(spotbugs_unmatched_table)
    rbugs_unmatched_csv_writer.writerows(rbugs_unmatched_table)



def convert_time(t):
    parts = t.split()
    format_time = ''
    if parts[1] == 's':
        format_time = '00:00:{}'.format(parts[0])
    elif parts[1] == 'min':
        format_time = '00:{}'.format(parts[0])
    elif parts[1] == 'h':
        format_time = '{}:00'.format(parts[0])
    parts = format_time.split(':')
    return float(parts[0])*60*60 + float(parts[1])*60 + float(parts[2])


if __name__ == '__main__':
    md = match()
    get_result(md)
    analyze_rbugs_report()
    # write_rbugs_execute_result()
    # write_speed_up()
    write_match_result(md)

    # # sum
    # sum_rbugs = 0
    # sum_spotbugs = 0
    # for key, value in csv_content_dict.items():
    #     sum_rbugs += len(value['rbugs_csv'])
    #     sum_spotbugs += len(value['spotbugs_csv'])
    # print('sum_rbugs', sum_rbugs)
    # print('sum_spotbugs', sum_spotbugs)
    # print('sum_both', len(csv_content_dict.keys()))


