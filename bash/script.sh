#!/bin/bash
sleep 15
ps aux | grep -i "wait"
echo "$?"
if ps aux | grep -i "wait"; then echo "Killing process wait.py..."; else echo "Not found"; fi
