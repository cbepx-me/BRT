#!/bin/bash

. /mnt/mod/ctrl/configs/functions &>/dev/null 2>&1
progdir=$(cd $(dirname "$0"); pwd)/b_r_tool

program="python3 ${progdir}/main.py"
log_file="${progdir}/log.txt"

$program > "$log_file" 2>&1
