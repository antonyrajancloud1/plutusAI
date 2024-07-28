#!/bin/bash

# Function to check if a service is active and start it if it's down
check_and_start_service() {
    local service_name=$1
    echo "Checking $service_name service..."
    if ! systemctl is-active --quiet $service_name; then
        echo "$service_name is not running. Starting $service_name..."
        if systemctl start $service_name; then
            echo "$service_name started successfully."
        else
            echo "Failed to start $service_name."
        fi
    else
        echo "$service_name is already running."
    fi
}

# Function to start a process in the background
start_process() {
    local process_command=$1
    local log_file=$2
    local process_name=$(echo $process_command | awk '{print $1}')

    if pgrep -f "$process_command" > /dev/null; then
        echo "$process_name is already running."
    else
        echo "Starting $process_name..."
        if [ -n "$log_file" ]; then
            nohup $process_command > $log_file 2>&1 &
        else
            nohup $process_command &
        fi

        if [ $? -eq 0 ]; then
            echo "$process_name started successfully."
        else
            echo "Failed to start $process_name."
        fi
    fi
}

# Main script
check_and_start_service mysql
check_and_start_service redis-server
start_process "python3 manage.py runserver 0.0.0.0:8000" "django.log"
start_process "celery -A plutus.celery worker -l info --concurrency=20"

# Create a named pipe to capture cloudflared output
fifo=$(mktemp -u)
mkfifo "$fifo"
trap "rm -f $fifo" EXIT

cloudflared tunnel --url http://localhost:8000 > "$fifo" 2>&1 &

# Capture the output in a background process
output=""
while read -r line; do
    #echo "$line"
    output+="$line"$'\n'
    if echo "$line" | grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' > /dev/null; then
        url=$(echo "$line" | grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com')
        python3 Informer.py $url
        echo $url
    fi
done < "$fifo" &

