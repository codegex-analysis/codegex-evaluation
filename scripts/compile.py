# 编译
import os, sys, stat, argparse
from subprocess import Popen, PIPE
import shutil
sys.path.append(os.path.dirname(__file__))
import utils
import csv

path_base = None
log_compile = None
skip_list = None
compile_list = None
is_force = None
is_purge = None

def parse_args():
    global path_base, log_compile, skip_list, compile_list, is_force, is_purge
    parser = argparse.ArgumentParser()
    parser.add_argument('-cl', '--compiles', help='list project names that need to compile. "," as delimiter')
    parser.add_argument('-ca', '--clear-all', dest='clear_all', action='store_true', help='clear all history data.')
    parser.set_defaults(clear_all=False)
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='forcely execute no matter whether '
                                                                                 'compile successfully before.')
    parser.set_defaults(force=False)
    parser.add_argument('-p', '--purge', dest='purge', action='store_true', help='purge local repository')
    parser.set_defaults(purge=False)
    args = parser.parse_args()
    path_base = utils.get_path_base()
    log_base = utils.get_log_base()
    compile_list = utils.get_list(args.compiles, path_base, 'compile')
    clear_all = args.clear_all
    is_force = args.force
    is_purge = args.purge
    if is_purge:
        log_compile = os.path.join(log_base, 'compile')
    else:
        log_compile = os.path.join(log_base, 'compile_')
    skip_list = utils.get_skips('compile')
    utils.clear_data(clear_all, log_compile)
    if not os.path.exists(log_compile):
        os.mkdir(log_compile)
    print("[path] {}".format(log_compile))
    print('project status time')

def start_compile():
    for filename in compile_list:
        logfile = os.path.join(log_compile, filename + '.log')
        cwdpath = os.path.join(path_base, filename)
        status = utils.get_compilation_status(logfile)
        time = utils.get_time(logfile)
        if not os.path.exists(logfile) or is_force:
            if is_purge:
                out, err = Popen(
                    ["mvn", "clean", "install", '-DskipTests=true', '-Dgpg.skip=true', '-Drat.skip=true',
                    '-Dmaven.javadoc.skip=true', '-fn', '-B' 'dependency:purge-local-repository'], cwd=cwdpath, stdout=PIPE,
                    stderr=PIPE).communicate()
            else:
                out, err = Popen(
                    ["mvn", "clean", "install", '-DskipTests=true', '-Dgpg.skip=true', '-Drat.skip=true',
                    '-Dmaven.javadoc.skip=true', '-fn', '-B'], cwd=cwdpath, stdout=PIPE,
                    stderr=PIPE).communicate()
            writefile = open(logfile, 'wb')
            writefile.write(out)
            writefile.write(err)
            writefile.close()
            status=utils.get_compilation_status(logfile)
            time = utils.get_time(logfile)
        print(filename, status, time)
    write_compile_result(compile_list)


def write_compile_result(compile_list):
    fail_pros = list()
    result_log = os.path.join(log_compile, 'compile-result.csv')
    csv_writer = csv.writer(open(result_log, 'w'))
    csv_table = [['project name', 'compile status', 'compile time']]
    for filename in compile_list:
        logfile = os.path.join(log_compile, filename + '.log')
        status = utils.get_compilation_status(logfile)
        time = utils.get_time(logfile)
        csv_table.append([filename, status, time])
    print('[save]', result_log)
    csv_writer.writerows(csv_table)

if __name__ == '__main__':
    parse_args()
    start_compile()

