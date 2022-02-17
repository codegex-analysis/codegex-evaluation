import os
import argparse
import sys
sys.path.append(os.path.dirname(__file__))
import utils
from subprocess import Popen, PIPE

path_base = None
log_execute = None
log_report = None
collect_list = None

def parse_args():
    global path_base, log_execute, log_report, collect_list
    parser = argparse.ArgumentParser()
    parser.add_argument('-cl', '--collects', help='list project names that need to collect bug reports. "," as delimiter')
    parser.add_argument('-ca', '--clear-all', dest='clear_all', action='store_true', help='clear history data.')
    parser.set_defaults(clear_all=False)
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='forcely execute no matter whether '
                                                                                 'compile successfully before.')
    parser.set_defaults(force=False)
    args = parser.parse_args()
    clear_all = args.clear_all

    path_base = utils.get_path_base()
    log_base = utils.get_log_base()
    log_execute = os.path.join(log_base, "execute")
    log_report = os.path.join(log_base, "report", 'spotbugs')
    utils.clear_data(clear_all, log_report)
    if not os.path.exists(log_report):
        os.mkdir(log_report)
    collect_list = utils.get_list(args.collects, log_execute, 'collect')
    print("[Path] {}".format(log_execute))

def collect():
    # 收集spotbugs中间文件
    print('Start collecting SpotBugs report from {} projects.'.format(str(len(collect_list))))
    print('[Projects] {}'.format(str(collect_list)))
    success_list = list()
    failure_dict = dict()
    for item in collect_list:
        ## debug
        status = utils.get_execution_status(os.path.join(log_execute, '{}.log'.format(item)))
        if status == "SUCCESS":
            print("Collecting {} ...".format(item))
            success_list.append(item)
            pipe = Popen(["find", os.path.join(path_base, item), "-name", "spotbugsXml.xml"], stdout=PIPE);
            allSpotbugsXml = pipe.communicate()[0].decode("utf-8").splitlines()
            print('[allSpotbugsXml length]', str(len(allSpotbugsXml)))
            for xmlFile in allSpotbugsXml:
                new_path = xmlFile.replace(path_base, log_report).replace(
                    "/target", "")
                pipe = Popen(["mkdir", "-p", new_path[0: new_path.rindex("/")]], stderr=PIPE, stdout=PIPE)
                pipe.communicate()
                pipe = Popen(["cp", xmlFile, new_path], stderr=PIPE, stdout=PIPE)
                pipe.communicate()
        else:
            if status in failure_dict.keys():
                failure_dict.get(status).append(item)
            else:
                failure_dict[status] = [item]

    print()
    print("Collection done. ")
    print("Total files: {}".format(str(len(collect_list))))
    print("Success files: {}".format(str(len(success_list))))
    print("Failure files. {}".format(str(failure_dict)))


if __name__ == '__main__':
    parse_args()
    collect()