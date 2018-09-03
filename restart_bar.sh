#!/bin/sh

pid=$(pgrep -f "python3.7 -m bar")

# Send USR1 to the process, not really an issue if we send to the wrong
# process because the process *probably* won't respond to USR1

kill -s USR1 $pid
