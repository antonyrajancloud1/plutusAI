#!/bin/bash

# Function to check if a service is active and start it if it's down
check_and_start_service() {
    service_name=$1
    echo "Checking $service_name service..."
    if ! service "$service_name" status > /dev/null 2>&1; then
        echo "$service_name is not running. Starting $service_name..."
        if service "$service_name" start; then
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
    process_command="$1"
    log_file="$2"
    process_name=$(echo "$process_command" | awk '{print $1}')

    if pgrep -f "$process_command" > /dev/null; then
        echo "$process_name is already running."
    else
        echo "Starting $process_name..."
        if [ -n "$log_file" ]; then
            nohup $process_command > "$log_file" 2>&1 &
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
start_process "sudo xvfb-run python3 manage.py runserver 0.0.0.0:80" "django.log"
start_process "celery -A plutus.celery worker -l info  --autoscale=100,1"
