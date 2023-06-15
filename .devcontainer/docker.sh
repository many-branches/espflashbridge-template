#!/bin/bash
echo "Starting custom docker..."
ehco "Launched" > launch.txt
./.flashbridge/server.sh &
docker $@