#!/bin/bash

# nohup sh inotifywait.sh > generate.log 2>&1 &

MONITOR_DIR=$(pwd)   # 监控路径
INOTIFYWAIT_BIN=/home/ryanxjli/data/inotify/bin/inotifywait     # inotifywait路径
PYTHON_BIN=/home/ryanxjli/miniconda2/envs/mypython3/bin/python  # python路径

while :
  do
  /home/ryanxjli/data/inotify/bin/inotifywait --exclude ${MONITOR_DIR}'/(generated|\.vscode|.*/README\.md|.*/*\.log|.*/*\.py|.*/*\.sh)' -rq -e modify,move_self,delete,move,close_write $MONITOR_DIR |
    while read event;
      do
      ${PYTHON_BIN} generate.py
      done
  done
