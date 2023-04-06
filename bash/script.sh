#!/bin/bash
sleep 15
pgrep -x "python ./python/wait.py"
echo "$?"
if pgrep "python ./python/wait.py"; then python ../python/message.py; else echo "Tests concluded"; fi
