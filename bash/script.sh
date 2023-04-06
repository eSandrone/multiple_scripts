#!/bin/bash
sleep 15
ps aux | grep -i "wait.py"
echo "$?"
if ps aux | grep -i "wait.py"; then echo "Killing process wait.py..."; else echo "Not found"; fi
