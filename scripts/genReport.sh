#!/bin/bash -e
function run()
{
    SPOTBUGS_COMPILE_LOG_PATH="/home/codegex/Documents/workspace/rbugs/experiment/log/compile"
    SPOTBUGS_COMPILE_LOG_PATH="/home/codegex/Documents/workspace/rbugs/experiment/log/execute"
    RBUGS_EXECUTE_LOG_PATH="/home/codegex/Documents/workspace/rbugs/experiment/log/report/rbugs/time.log"
    outputTable $COMPILE_LOG_PATH, $SPOTBUGS_COMPILE_LOG_PATH
    source util.bash; printTable ',' "$(cat data.txt)"
}

function outputTable()
{
#     # echo "ProjName, SBComTime, SBExeTime, RBExeTime, ComSpeedUp, ExeSpeedUp" > data.txt
#     echo "ProjName, SBComTime, RBExeTime, SpeedUp" > data.txt
#     for filename in "$SPOTBUGS_COMPILE_LOG_PATH"/*; do
#         basename=`echo $(basename $filename) | cut -d'.' -f 1`
#         spotbugs_compile_time=`grep "\[INFO\] Total time" "$filename" | tail -1 | awk -F': ' '{if ($0=="") print "0"; else print $2}'`
        
#         # echo "$spotbugs_execute_time"
#         # echo "$rbugs_execute_time"
#         spotbugsFormatTime=$(convertTime "$spotbugs_execute_time")
#         rbugsFormatTime=$(convertTime "$rbugs_execute_time")

# #        echo "$spotbugs_execute_time, $spotbugsFormatTime"
# #        echo "$rbugs_execute_time, $rbugsFormatTime"
#         speedup="`echo "scale=2; $spotbugsFormatTime/$rbugsFormatTime" | bc -l`"
#         echo "$basename, $spotbugs_compile_time, $spotbugs_execute_time, $rbugs_execute_time, $speedup" >> data.txt
#     echo "ProjName, SBExeTime, RBExeTime, SpeedUp" > data.txt
#     for filename in "$SPOTBUGS_COMPILE_LOG_PATH"/*; do
#         if [ "`grep "\[INFO\] BUILD SUCCESS" "$filename" | wc -l`" -eq "0" ]; then
#             spotbugs_execute_time=`grep "Total time" "$filename" | awk -F': ' '{if ($0=="") print "0"; else print $2}'`
#         fi
#         rbugs_execute_time=`grep "$basename" "$RBUGS_EXECUTE_LOG_PATH" |  cut -d' ' -f2- | xargs | sed 's/seconds/s/g'`
#     done
    # echo "ProjName, SBComTime, SBExeTime, RBExeTime, ComSpeedUp, ExeSpeedUp" > data.txt
}

function convertTime()
{
    if [ -z "$1" ]; then
        echo "0"
    fi
    sentence=$1
    tokens=($sentence)
    if [[ "${tokens[1]}" == "s" ]]; then
        echo "00:00:${tokens[0]}" | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }'
    elif [[ ${tokens[1]} == "min" ]]; then
        echo "00:${tokens[0]}" | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }'
    else
        echo "${tokens}:00" | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }'
    fi
}

rootdir="/home/codegex/Documents/workspace/log/execute"
run $*
