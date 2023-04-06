#!/bin/bash
sleep 15
ps aux | grep -i "wait.py"
echo "$?"
pgrep "wait.py"
echo "$?"
if pgrep "wait.py"; then echo "Killing process wait.py..."; else echo "Not found"; fi
