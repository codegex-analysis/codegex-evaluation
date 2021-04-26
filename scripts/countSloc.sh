#!/bin/bash
eval "$(conda shell.bash hook)"
function run()
{
    conda activate myenv3
    repos_path="/home/codegex/Documents/workspace/rbugs/experiment/top100repos"
    log_path="/home/codegex/Documents/workspace/rbugs/experiment/log/sloc"
    echo "Start counting sloc ..."
    rm "$log_path/"*
    for filename in "$repos_path"/*; do
        logfile="$log_path/$( basename $filename ).log"
        pygount --suffix=java --format=summary $filename > $logfile
        echo "[Project Done] $( basename $filename )"
    done
}

function analyze()
{
    log_path="/home/codegex/Documents/workspace/rbugs/experiment/log/sloc"
    $(grep -r "Sum total" "$log_path")
    IFS=$'\n'
    for line in $(grep -r "Sum total" "$log_path"); do
        projname=$(echo "$line" | cut -d':' -f 1)
        basename=$(echo $( basename $projname ) | cut -d'.' -f 1)
        codelinescnt=$(echo "$line" | cut -d':' -f 2 | tr -s ' ' | cut -d' ' -f 4)
        echo "$basename, $codelinescnt"
    done
}

analyze
