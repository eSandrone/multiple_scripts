#!/bin/bash
sleep 15
pgrep "wait.py"
echo "$?"
if pgrep "wait.py"; then python ../python/message.py; else echo "Tests concluded"; fi
