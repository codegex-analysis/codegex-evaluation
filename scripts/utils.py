
import shutil
import configparser
import os
from subprocess import Popen, PIPE
import csv

configParser = configparser.ConfigParser()
configFilePath = "config.txt"
configParser.read(configFilePath)
path_base = configParser.get('general', 'path')
log_base = configParser.get('general', 'log')

def get_skips(type):
    skips = configParser.get('general', "{}_skips".format(type))
    if skips is not None:
        return skips.split(',')
    else:
        return list()

def get_path_base():
    return path_base

def get_log_base():
    return log_base

def get_list(str, path, type):
    if str is not None:
        return str.split(',')
    else:
        newlist = list()
        if type == 'compile':     
            return [proj_name for proj_name in os.listdir(path)]
        elif type == 'execute':
            compile_csv_path = os.path.join(log_base, 'compile', 'compile-result.csv')
            return [row[0] for row in csv.reader(open(compile_csv_path, 'r')) if row[1] == 'SUCCESS']
        elif type == 'collect':
            return [os.path.basename(filename).replace('.log', '') for filename in os.listdir(path)]
        elif type == 'modify':
            return [proj_name for proj_name in os.listdir(path)]

def clear_data(clear, path):
    if clear and os.path.exists(path):
        shutil.rmtree(path)
        print("[Clear] done. -- {}".format(path))

def get_execution_status(log_path):
    if not os.path.exists(log_path):
        return "UNSTATED"
    f = open(log_path, 'r')
    content = f.read()
    if os.path.getsize(log_path) == 0:
        return "UNFINISHED"
    # if "Exception analyzing" in content or "Exception in" in content:
    #     return "EXCEPTION"
    if "Timeout: killed the sub-process" in content:
        return "TIMEOUT"
    return "SUCCESS"

def get_compilation_status(log_path):
    if not os.path.exists(log_path):
        return "UNSTATED"
    out, err = Popen('grep -h \"\[INFO\] BUILD\" {} | tail -1'.format(log_path), stdout=PIPE, stderr=PIPE, shell=True).communicate()
    if 'FAILURE' in out.decode():
        return 'FAILURE'
    elif 'SUCCESS' in out.decode():
        return 'SUCCESS'
    else:
        return '-'

def get_time(log_path):
    if not os.path.exists(log_path):
        return "-"
    out, err = Popen('grep -h "\[INFO\] Total time:" {} | tail -1 | cut -d \' \' -f5-'.format(log_path), stdout=PIPE, stderr=PIPE, shell=True).communicate()
    if out.decode().strip() == '':
        return '-'
    return out.decode().strip()