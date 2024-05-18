#!/bin/bash

# Loop through each line of the output
while read -r line; do
    # Extract container ID and name
    container_id=$(echo "$line" | awk '{print $1}')
    container_name=$(echo "$line" | awk '{print $NF}')

    # Delete the container
    docker rm -f "$container_id"

    # Check if deletion was successful
    if [ $? -eq 0 ]; then
        echo "Container '$container_name' ($container_id) deleted successfully."
    else
        echo "Failed to delete container '$container_name' ($container_id)."
    fi
done <<< "$(docker ps -a | grep Exited)"


