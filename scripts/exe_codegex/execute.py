#%%
from pathlib import Path
import os
import re
from subprocess import check_output, Popen, PIPE
import json
import time
import csv

from codegex.models.context import Context
from codegex.models.engine import DefaultEngine
from codegex.utils.rparser import parse


# Path(__file__).resolve() guarantee to return absolute path, while __file__ must gives absolute path only in Python 3.9 or later versions 
path_cur_dir = Path(__file__).resolve().parent  # invoke resolve() to get absolute path
path_root = path_cur_dir.parent.parent
path_top100_repos = path_root / "top100repos"

path_sp_exepath = path_root / "log" / "exepath"

path_log = Path(__file__).resolve().parent / "log"
path_report = path_log / "report"
path_exejson = path_log / "exejson"

os.makedirs(path_log, exist_ok=True)
os.makedirs(path_report, exist_ok=True)
os.makedirs(path_exejson, exist_ok=True)


JAVA_FILE_PATTERN = re.compile(r'^(.+?)/src/(main|test)/java/')
ANALYZE_FILE = re.compile(r'\[java\] \w+\s+\d+: Analyzing classes \(')

#%%
#########################
# Step 1
#########################
def gen_analyze_paths():
    """
    Get SpotBugs' analyzed files according to its log files
    """
    ls_result = os.listdir(path_sp_exepath)
    # Notice: DON't use rstrip(".log") to trim suffix since ".log" are treated as a character list instead of a substring
    project_names = [name[:-4] for name in ls_result if name.endswith('.log')]

    for name in project_names:
        files_to_analyze = set()
        with open(path_sp_exepath / f'{name}.log', 'r') as f:
            for line in f:
                line = line.strip()
                if ANALYZE_FILE.match(line):
                    tmp = line.split()
                    if tmp:
                        output = check_output(['find', path_top100_repos / name, '-path', f'*{tmp[-1]}.java']).decode('utf-8')
                        if output.strip():
                            for p in output.splitlines():
                                if '/src/main/java/' in p or '/src/test/java/' in p:
                                    files_to_analyze.add(p.strip())
        if files_to_analyze:
            with open(path_exejson / f'{name}.json', 'w') as out:
                json.dump(list(files_to_analyze), out)
#########################
# Helper Methods
#########################

def exec_task(file_list):
    bug_instances = list()
    context = Context()
    engine = DefaultEngine(context)

    # generate patch set
    patchset = []
    for file_path in file_list:
        with open(file_path, 'r') as f:
            patch = parse(f.read(), is_patch=False, name=file_path)
            patchset.append(patch)

    # run detectors
    if patchset:
        engine.visit(*patchset)
        bug_instances = engine.filter_bugs(level='low')

    return bug_instances


def detect_project(project_name: str):
    repo_exejson = path_exejson / f'{project_name}.json'
    if not repo_exejson.exists():
        return False

    # load files to analyze
    with open(repo_exejson, 'r') as f:
        path_list = json.load(f)

    if path_list:
        # analyze files
        bug_instances = exec_task(path_list)

        # write reports
        if bug_instances:
            repo_report_path = path_report / project_name
            os.makedirs(repo_report_path, exist_ok=True)
            # write csv
            rows = list()
            for ins in bug_instances:
                rows.append([ins.type, ins.file_name, ins.line_no, ins.line_content])

            with open(f'{repo_report_path}/{project_name}.csv', 'w') as out:
                csv_writer = csv.writer(out)
                csv_writer.writerows(rows)

            # write bug instance json
            with open(f'{repo_report_path}/bug_instances.json', 'w') as out:
                bugs_json = dict()
                bugs_json['repo'] = project_name
                bugs_json['total'] = len(bug_instances)
                bugs_json['items'] = [bug.__dict__ for bug in bug_instances]
                json.dump(bugs_json, out)

    return True


#########################
# Helper Structures
#########################

KEY_LIST = 'elapsed_time_list'
KEY_AVG = 'average'


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class AverageTimer:
    timers = dict()  # shared by all timers

    def __init__(
        self,
        name=None,
        text="Elapsed time: {:0.4f} seconds",
        logger=print,
    ):
        self._start_time = None
        self.name = name
        self.text = text
        self.logger = logger

        # Add new named timers to dictionary of timers
        if self.name:
            self.timers[self.name] = {KEY_LIST: list(), KEY_AVG: 0}

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        # update timers
        if self.name:
            self.timers[self.name][KEY_LIST].append(elapsed_time)
            time_list = self.timers[self.name][KEY_LIST]
            self.timers[self.name][KEY_AVG] = sum(time_list)/len(time_list)

        return elapsed_time


#########################
# Step 2
#########################
def main_loop():
    EXE_TIMES = 5
    project_name_list = os.listdir(path_top100_repos)
    for project_name in project_name_list:
        project_timer = AverageTimer(name=project_name, logger=None)

        is_detected = False
        for _ in range(EXE_TIMES):
            # remove old report
            path_project = path_report / project_name
            if path_project.exists():
                p = Popen(['rm', '-r', path_project], stdout=PIPE)  # Asynchronous, non-blocking
                out, _ = p.communicate()  # block util p return

            # generate new report
            project_timer.start()
            is_detected = detect_project(project_name)
            project_timer.stop()
        if not is_detected:
            del project_timer.timers[project_name]

    # write time dict to file
    with open(path_report / "time.json", 'w') as out:
        json.dump(AverageTimer.timers, out)

#%%
if __name__ == '__main__':
    # gen_analyze_paths()
    main_loop()
# %%
