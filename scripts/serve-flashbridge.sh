#!/bin/bash
export FLASH_BRIDGE_PORT
# Run ./.flashbridge/server.sh in the background and redirect output to a log file
echo "Starting new service in background"
nohup ./.flashbridge/server.sh > server.log 2>&1 &
