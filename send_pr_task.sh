#!/bin/bash
# Simple script to send PR tasks to Claude

# Check if task type is provided
if [ $# -eq 0 ]; then
    echo "Usage: ./send_pr_task.sh <task_type>"
    echo "Available tasks: readme, api_docs, type_safety, test_coverage, code_cleanup, error_handling"
    exit 1
fi

TASK_TYPE=$1

# Run the Python script
python3 trigger_pr_task.py "$TASK_TYPE"