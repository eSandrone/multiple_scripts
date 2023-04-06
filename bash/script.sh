#!/bin/bash
sleep 15
pgrep "wait"
echo "$?"
if pgrep "wait"; then python ../python/message.py; else echo "Tests concluded"; fi
