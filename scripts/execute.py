import os
import sys
import argparse
from subprocess import Popen, PIPE
sys.path.append(os.path.dirname(__file__))
import utils
import csv

path_base = None
log_execute = None
skip_list = None
execute_list = None
is_force = None
exepath = None
is_filter = None

def parse_args():
    global path_base, log_execute, skip_list, execute_list, is_force, exepath, is_filter
    parser = argparse.ArgumentParser()
    parser.add_argument('-el', '--executes', help='list project names that need to executes. "," as delimiter')
    parser.add_argument('-ca', '--clear-all', dest='clear_all', action='store_true', help='clear history data.')
    parser.set_defaults(clear_all=False)
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='forcely execute no matter whether '
                                                                                 'execute successfully before.')
    parser.add_argument('-ep', '--exepath', dest='exepath', action='store_true', help='get spotbugs analyzed classes')
    parser.add_argument('-nf', '--no-filter', dest='filter', action='store_false')
    parser.set_defaults(filter=True)
    args = parser.parse_args()
    clear_all = args.clear_all
    is_force = args.force
    is_filter = args.filter
    path_base = utils.get_path_base()
    log_base = utils.get_log_base()
    exepath = args.exepath
    if args.exepath:
        log_execute = os.path.join(log_base, 'exepath')
    elif not is_filter:
        log_execute = os.path.join(log_base, 'execute_')
    else:
        log_execute = os.path.join(log_base, 'execute')
    execute_list = utils.get_list(args.executes, path_base, 'execute')
    skip_list = utils.get_skips('execute')
    utils.clear_data(clear_all, log_execute)
    if not os.path.exists(log_execute):
        os.mkdir(log_execute)
    print("[Log Path] {}".format(log_execute))

def remove_invalid_file():
    # 删除空文件
    proc = Popen("find . -type f -size 0 -print -delete".split(" "), cwd=log_execute, stderr=PIPE,
                 stdout=PIPE).communicate()
    if len(proc[0]) != 0:
        print("[DELETE] empty files: {}".format(proc[0].decode()))
    # 刪除未執行完文件
    proc = Popen("find . -type f -print0 | xargs --null grep -Z -L 'Total time' | xargs --null rm ".split(" "),
                 cwd=log_execute, stderr=PIPE, stdout=PIPE).communicate()


def execute_maven():
    remove_invalid_file()
    # 构建成功 execute SpotBugs
    print('Start executing SpotBugs at {} projects. exepath: {}'.format(str(len(execute_list)), str(exepath)))
    print('[Projects] {}'.format(str(execute_list)))
    for filename in execute_list:
        logpath = os.path.join(log_execute, filename + '.log')
        cwdpath = os.path.join(path_base, filename)
        status = utils.get_execution_status(logpath)
        if status == "SUCCESS" and not is_force:
            print('[SKIP] {} ... {}'.format(os.path.basename(filename), status))
            continue
        openfile = open(logpath, 'wb')
        Popen(["mvn", "com.github.spotbugs:spotbugs-maven-plugin:4.2.3-SNAPSHOT:check", "-fn", "-B"], cwd=cwdpath, stdout=openfile,
              stderr=openfile).communicate()
        # Popen(["mvn", "site"], cwd=cwdpath, stdout=logfile, stderr=logfile).communicate()
        status = utils.get_execution_status(logpath)
        print('[EXECUTE] {} ... {}'.format(os.path.basename(filename), status))

def write_execute_result():
    compile_csv_path = os.path.join(log_execute.replace('execute', 'compile'), 'compile-result.csv')
    csv_table = [row for row in csv.reader(open(compile_csv_path, 'r'))]
    for line_no, row in enumerate(csv_table):
        if line_no == 0:
            csv_table[line_no] = row + ['spotbugs execute status', 'spotbugs execute time']
        else:
            if row[1] != 'SUCCESS':
                csv_table[line_no] = row + ['-', '-']
            else:
                logfile = os.path.join(log_execute, row[0] + '.log')
                status = utils.get_execution_status(logfile)
                time = utils.get_time(logfile)
                csv_table[line_no] = row + [status, time]
    result_log = os.path.join(log_execute, 'execute-result.csv')
    csv_writer = csv.writer(open(result_log, 'w'))
    csv_writer.writerows(csv_table)


if __name__ == '__main__':
    parse_args()
    execute_maven()
    if not exepath:
        write_execute_result()


## help command
# grep -l "Timeout: killed the sub-process" *.log | sed 's/. log//g'| paste -sd "," -