#!/bin/bash
if [[ "$FLASH_MODE" == "ssh" ]]; then
ssh -t $HOST_USER@$HOST_HOSTNAME "/bin/bash -c 'espflash flash --monitor $1'"
elif [[ "$FLASH_MODE" == "server" ]]; then
./.flashbridge/client.sh flash --monitor $1 --port $FLASH_PORT
else
espflash flash --monitor $1
fi

