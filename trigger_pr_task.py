#!/usr/bin/env python3
"""
Script to trigger PR creation tasks for Claude
"""

import requests
import json
import sys
import time

# API endpoint
API_URL = "https://www.autonomous.claudecode.fun/api/agent/command"

def send_command(prompt: str):
    """Send a command to Claude via the API"""
    try:
        response = requests.post(
            API_URL,
            json={"command": prompt, "parameters": {}},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Command sent successfully")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Failed to send command: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending command: {e}")
        return False

# PR Task Templates
PR_TASKS = {
    "readme": """I'll help you create a pull request to improve the README.md file. Let me start by setting up the repository and examining the current documentation.

First, I'll navigate to the claude-computer repository (which should already be cloned at ~/claude-computer thanks to the startup script), create a new branch, and analyze the README to identify improvements.

I'll focus on:
- Adding missing sections (if any)
- Improving clarity and structure
- Adding helpful badges and status indicators
- Ensuring all instructions are up-to-date

Let me begin by checking the repository status and creating a new feature branch.""",

    "api_docs": """I'll create a pull request to document all API endpoints. Let me start by examining the backend code to catalog all available endpoints.

I'll open a terminal, navigate to ~/claude-computer, create a new branch for API documentation, and analyze backend/main.py to document:
- All endpoint paths and HTTP methods
- Request/response schemas with examples
- Authentication requirements
- Error responses

I'll create a comprehensive docs/API.md file with clear, developer-friendly documentation.""",

    "type_safety": """I'll create a pull request to improve TypeScript type safety in the frontend code. Let me examine the codebase to find areas that need better typing.

I'll navigate to ~/claude-computer/frontend, create a new branch, and search for:
- Components using 'any' type
- Missing interface definitions  
- Implicit any errors
- Areas where we can add stricter types

I'll focus on one or two components to keep the PR focused and easy to review.""",

    "test_coverage": """I'll create a pull request to add unit tests for an untested backend module. Let me explore the backend code to identify modules that need test coverage.

I'll check ~/claude-computer/backend for Python modules without corresponding test files, then:
- Create proper test file structure
- Write comprehensive pytest-based unit tests
- Add fixtures for test data
- Ensure the tests are meaningful and cover edge cases

I'll focus on one module to keep the PR manageable.""",

    "code_cleanup": """I'll create a pull request to refactor and clean up code. Let me analyze the codebase to find a file that would benefit from cleanup.

I'll look for opportunities to:
- Remove commented-out or dead code
- Improve variable and function names for clarity
- Extract duplicated logic into reusable functions
- Add clarifying comments where complex logic exists
- Fix any linting issues

I'll keep the changes focused on one file or module.""",

    "error_handling": """I'll create a pull request to improve error handling in the codebase. Let me examine the code to find areas where error handling can be enhanced.

I'll search for places that need:
- Proper try/catch or try/except blocks
- More informative error messages
- Consistent error logging
- Graceful handling of edge cases

I'll focus on one module or component to ensure the PR remains reviewable."""
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python trigger_pr_task.py <task_type>")
        print(f"Available tasks: {', '.join(PR_TASKS.keys())}")
        sys.exit(1)
    
    task_type = sys.argv[1]
    
    if task_type not in PR_TASKS:
        print(f"Unknown task type: {task_type}")
        print(f"Available tasks: {', '.join(PR_TASKS.keys())}")
        sys.exit(1)
    
    prompt = PR_TASKS[task_type]
    
    print(f"🚀 Sending {task_type} PR task to Claude...")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    
    if send_command(prompt):
        print("\n✅ Task sent! Claude should now start working on the PR.")
        print("Monitor progress at: https://www.autonomous.claudecode.fun")
    else:
        print("\n❌ Failed to send task")

if __name__ == "__main__":
    main()