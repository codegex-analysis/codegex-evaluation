# How to install codegex

```shell
tar -zxvf codegex-0.1.0.tar.gz
cd codegex-0.1.0
python setup.py install
```

# How to run experiments

`execute.py`

#### Step 1. Generate analyzing paths

Invoke method `gen_analyze_paths()`, the output will be written under `./local/exejson`

#### Step 2. Run codegex

Invoke method `main_loop()` which will execute codegex against repos five times. Modify ``path_top100_repos`` where you store the repos.

- The time info is in `./log/report/time.json`
- Full report is under `./log/report`

# Get Incremental Report

`filter.py`

It will extract bug instances of pattern types in `new_patterns.txt` and output is under `./log/incremental_report/instances.csv`.
