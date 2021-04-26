import csv

sloc_dict = dict()


def load_sloc():
    sloc_file = [line.strip() for line in open('config/sloc.txt', 'r').readlines()]
    for line in sloc_file:
        parts = line.split(',')
        sloc = round(int(parts[1]) / float(1000), 2)
        sloc_dict[parts[0]] = sloc


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
    return round(float(parts[0]) * 60 * 60 + float(parts[1]) * 60 + float(parts[2]), 2)


def print_table():
    csv_file = csv.reader(open('../../../log/report/comparison-result-speedup.csv', 'r'))
    csv_table = [row for row in csv_file]
    unique_proj = set()
    rows = []
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            continue
        compile_status = row[1]
        if compile_status == 'SUCCESS':
            project = row[0]
            temp = project
            if len(project) > 20:
                temp = '-'.join(project.split('-')[:2])
                if temp in unique_proj:
                    temp = '-'.join(project.split('-')[:3])
                    if temp in unique_proj:
                        print('duplicate project name')
            unique_proj.add(temp)
            compile_time = convert_time(row[2])
            compile_time_np = convert_time(row[3])
            spotbugs_execute_time = convert_time(row[5])
            codegex_execute_time = convert_time(row[6])
            if codegex_execute_time == 0:
                speed_up = round((compile_time + spotbugs_execute_time) / 0.01, 2)
                speed_up_np = round((compile_time_np + spotbugs_execute_time) / 0.01, 2)
                speed_up_nc = round(spotbugs_execute_time / 0.01, 2)
                row = ('%s, %.02f, %.02f, %.02f, %.02f, <0.01, %.02f, %.02f, %.02f' % (temp, sloc_dict[project],
                                                                                       compile_time, compile_time_np,
                                                                                       spotbugs_execute_time, speed_up,
                                                                                       speed_up_np,
                                                                                       speed_up_nc))
                rows.append(row.split(','))
            else:
                speed_up = round((compile_time + spotbugs_execute_time) / codegex_execute_time, 2)
                speed_up_np = round((compile_time_np + spotbugs_execute_time) / codegex_execute_time, 2)
                speed_up_nc = round(spotbugs_execute_time / codegex_execute_time, 2)
                row = ('%s, %.02f, %.02f, %.02f, %.02f, %.02f, %.02f, %.02f, %.02f' % (temp, sloc_dict[project],
                                                                                       compile_time, compile_time_np,
                                                                                       spotbugs_execute_time,
                                                                                       codegex_execute_time, speed_up,
                                                                                       speed_up_np, speed_up_nc))
                rows.append(row.split(','))
    sums = [0] * 8
    for row in rows:
        sums = [sums[i] + 0.01 if row[i+1].strip() == '<0.01' else sums[i] + float(row[i+1]) for i in range(len(sums))]
    rows.append(['Average'] + [round(sums[i] / float(52), 2) for i in range(len(sums))])
    rows = [['Project', 'SLOC', 'SpotBugs', '', '', 'CodeGex,SpeedUp', '', ''],
            ['', '', 'IC', 'SC', 'A', 'A', 'S1', 'S2', 'S3']] + rows
    csv.writer(open('config/project-speedup.csv', 'w')).writerows(rows)


if __name__ == '__main__':
    load_sloc()
    print_table()
