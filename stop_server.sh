#!/bin/bash

# Function to stop a process by name
stop_process_if_running() {
    local process_name=$1
    local pid=$(pgrep -f "$process_name")
    if [ -n "$pid" ]; then
        echo "Stopping $process_name with PID $pid"
        kill $pid  # Send SIGTERM to gracefully stop the process
        sleep 2  # Wait for the process to terminate gracefully
        # Check if the process is still running after waiting
        if ps -p $pid > /dev/null; then
            echo "$process_name with PID $pid did not stop gracefully. Sending SIGKILL."
            kill -9 $pid  # Forcefully terminate the process
        fi
    else
        echo "$process_name is not running."
    fi
}

# Stop Django server
stop_process_if_running "python3 manage.py runserver"

# Stop Celery worker
stop_process_if_running "celery -A madaraUI.celery worker"
