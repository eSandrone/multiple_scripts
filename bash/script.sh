#!/bin/bash
sleep 15
pgrep -l "./python/wait.py"
ps aux | grep -i "wait.py"
echo "$?"
if pgrep "python ./python/wait.py"; then python ../python/message.py; else echo "Tests concluded"; fi
