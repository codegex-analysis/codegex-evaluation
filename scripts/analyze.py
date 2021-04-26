from os import path, listdir, makedirs
import xml.etree.ElementTree as ET
import subprocess
import csv
import shutil
is_filter = False

if is_filter:
    SpotBugs_XML_BASE = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/spotbugs'
else:
    SpotBugs_XML_BASE = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/spotbugs_'
RBugs_REPORT_BASE = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/rbugs'
# RBUGS_REPORT_BASE = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/rbugs'
CSV_BASE = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/csv'
makedirs(CSV_BASE, exist_ok=True)
max_prioprity = 3 #Low


# MERGE_CSV_BASE = '/home/codegex/Documents/workspace/rbugs/experiment/log/report/merge_csv'

# makedirs(MERGE_CSV_BASE, exist_ok=True)


CSV_BASE_LOG = path.join(CSV_BASE, 'error.log')
# MERGE_CSV_BASE_LOG = path.join(MERGE_CSV_BASE, 'error.log')

def parse_xml(file_path:str):
    tree = ET.parse(file_path)
    root = tree.getroot()
    bug_instances = list()
    for bug in root.findall('BugInstance'):
        bug_type = bug.attrib['type']
        source_line = bug.find('SourceLine')

        if 'start' not in source_line.attrib:
            start_line_no = -1
            with open(CSV_BASE_LOG, 'a') as f:
                attributes = ''
                for k, v in source_line.attrib.items():
                    attributes += f'\t{k}: {v}\n'
                f.write(f'[Start Not Found] {file_path}\n\t{bug_type}\n{attributes}')
        else:
            start_line_no = source_line.attrib['start']
        source_path = source_line.attrib['sourcepath']
        bug_instances.append((bug_type,source_path,start_line_no))
    return bug_instances


def gen_csv_from_xml(project_name: str):
    bugs = list()
    base_path = path.join(SpotBugs_XML_BASE, project_name)
    allSpotbugsXml = subprocess.check_output(["find", base_path, "-name", "*.xml"]).decode('utf-8')
    for xmlFile in allSpotbugsXml.splitlines():
        bugs.extend(parse_xml(xmlFile))

    if len(bugs) > 0:
        write_path = path.join(CSV_BASE, project_name)
        makedirs(write_path, exist_ok=True)
        if is_filter:
            write_path = path.join(write_path, 'spotbugs.csv')
        else:
            write_path = path.join(write_path, 'spotbugs_.csv')
        with open(write_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(bugs)


def col_csv_from_rbugs(project_name: str):

    # ------------------------------------------------------#
    original_csv_file = path.join(RBugs_REPORT_BASE, project_name, '{}.csv'.format(project_name))
    copy_csv_file = path.join(CSV_BASE, project_name, 'rbugs.csv')
    makedirs(copy_csv_file[:-9], exist_ok=True)
    try:
        subprocess.check_output(['cp', original_csv_file, copy_csv_file])
    except subprocess.CalledProcessError as cpe:
        print(cpe)

    # ------------------------------------------------------#
    # bugs = list()
    # bugs_filter = list()
    # base_path = path.join(RBugs_REPORT_BASE, project_name)
    # allMainCSV = check_output(["find", base_path, "-name", "main.csv"]).decode('utf-8')
    # allTestCSV = check_output(["find", base_path, "-name", "test.csv"]).decode('utf-8')
    # unique_set = set()
    # for csvFile in allMainCSV.splitlines():
    #     csv_reader = csv.reader(open(csvFile, 'r'))
    #     for row in csv_reader:
    #         key = ','.join(row)
    #         if key not in unique_set:
    #             unique_set.add(key)
    #             bugs.append(row)
    #             priority = int(row[1])
    #             if priority <= max_prioprity:
    #                 bugs_filter.append(row)

    # for csvFile in allTestCSV.splitlines():
    #     csv_reader = csv.reader(open(csvFile, 'r'))
    #     for row in csv_reader:
    #         key = ','.join(row)
    #         if key not in unique_set:
    #             unique_set.add(key)
    #             bugs.append(row)
    #             priority = int(row[1])
    #             if priority <= max_prioprity:
    #                 bugs_filter.append(row)

    # if len(bugs) > 0:
    #     proj_report_path = path.join(CSV_BASE, project_name)
    #     if not path.exists(proj_report_path):
    #         makedirs(proj_report_path)
    #     write_path = path.join(proj_report_path, 'rbugs-all.csv')
    #     with open(write_path, 'w') as f:
    #         writer = csv.writer(f)
    #         writer.writerows(bugs)
    # if len(bugs_filter) > 0:
    #     write_path = path.join(CSV_BASE, project_name, 'rbugs.csv')
    #     with open(write_path, 'w') as f:
    #         writer = csv.writer(f)
    #         writer.writerows(bugs_filter)



if __name__ == '__main__':
    # shutil.rmtree(CSV_BASE)
    #Generate csv from xml reports
    # spotbugs_proj_list = listdir(SpotBugs_XML_BASE)
    # for project in spotbugs_proj_list:
    #     gen_csv_from_xml(project)

    # Collect csv from rbugs reports 
    rbugs_proj_list = listdir(RBugs_REPORT_BASE)
    for project in rbugs_proj_list:
        if path.isdir(path.join(RBugs_REPORT_BASE, project)):
            col_csv_from_rbugs(project)
