#!/bin/bash

DISCORD_TOKEN="<token>"

echo "Starting dnd-buddy..."

docker run -d --rm -e DISCORD_TOKEN="${DISCORD_TOKEN}" --name dnd-buddy --entrypoint python buddy:latest /srv/dnd-buddy

if [[ $? -ne 0 ]]; then
    echo "Failed to start dnd-buddy"
    exit 1
fi

echo "dnd-buddy started!"
exit 0
