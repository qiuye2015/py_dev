#!/bin/bash
pid=$1
PIDS=`ps -aux | grep "$pid" | grep -v grep | grep -v monitor`
if [ "$PIDS" == ""  ]; then
    python mail.py
fi
