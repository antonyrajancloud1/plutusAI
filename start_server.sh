#!/bin/bash

# Function to check if a service is active and start it if it's down
check_and_start_service() {
    local service_name=$1
    echo "Checking $service_name service..."
    if service $service_name status > /dev/null 2>&1; then
        echo "$service_name is already running."
    else
        echo "$service_name is not running. Starting $service_name..."
        service $service_name start
        if [ $? -eq 0 ]; then
            echo "$service_name started successfully."
        else
            echo "Failed to start $service_name."
        fi
    fi
}

# Check if MySQL is running and start it if it's not
check_and_start_service mysql

# Check if Redis is running and start it if it's not
check_and_start_service redis-server

# Function to start a process in the background
start_process() {
    local process_command=$1
    local log_file=$2
    local process_name=$(echo $process_command | awk '{print $1}')
    local process_check=$(pgrep -f "$process_command")

    if [ -n "$process_check" ]; then
        echo "$process_name is already running."
    else
        echo "Starting $process_name..."
        nohup $process_command > $log_file 2>&1 &
        if [ $? -eq 0 ]; then
            echo "$process_name started successfully and is logging to $log_file."
        else
            echo "Failed to start $process_name."
        fi
    fi
}

# Start Django process in the background
start_process "python3 manage.py runserver 0.0.0.0:8000" "django.log"

# Start Celery process in the background
start_process "celery -A plutus.celery worker -l info" "celery.log"

