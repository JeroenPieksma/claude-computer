# PR Automation Guide

This guide explains how to trigger Claude to create pull requests for the claude-computer repository.

## Setup (Automated on VM Startup)

When the VM starts, the following happens automatically:

1. GitHub CLI is installed (if not present)
2. Git is configured with Claude's identity
3. GitHub authentication is set up (using GITHUB_TOKEN from .env)
4. The repository is cloned to `~/claude-computer`
5. PR instructions are created at `~/PR_INSTRUCTIONS.md`
6. Desktop shortcuts are created for easy access

## Triggering PR Tasks

### Method 1: Using the Shell Script (Simplest)

```bash
./send_pr_task.sh <task_type>
```

Available task types:
- `readme` - Improve README documentation
- `api_docs` - Create API documentation
- `type_safety` - Improve TypeScript types
- `test_coverage` - Add unit tests
- `code_cleanup` - Refactor and clean code
- `error_handling` - Improve error handling

Example:
```bash
./send_pr_task.sh readme
```

### Method 2: Using the Python Script

```bash
python3 trigger_pr_task.py <task_type>
```

### Method 3: Direct API Call

```bash
curl -X POST https://www.autonomous.claudecode.fun/api/agent/command \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Create a pull request to improve the README.md file...",
    "parameters": {}
  }'
```

## What Happens Next

1. Claude receives the command in the VM
2. Opens a terminal and navigates to the repository
3. Creates a new feature branch
4. Makes the requested improvements
5. Commits the changes with a descriptive message
6. Pushes the branch to GitHub
7. Creates a pull request using `gh pr create`

## Monitoring Progress

Watch Claude's progress at: https://www.autonomous.claudecode.fun

## PR Guidelines

Claude follows these guidelines when creating PRs:

- Keeps PRs small and focused (< 500 lines)
- Uses clear, descriptive commit messages
- Includes detailed PR descriptions
- Runs linting and tests before pushing
- Creates feature branches with descriptive names

## Environment Variables

Set in `.env`:
- `CLAUDE_AUTONOMOUS_MODE=false` - Ensures Claude only acts on commands
- `GITHUB_TOKEN` - Used for GitHub authentication
- `GITHUB_REPO` - Repository URL

## Troubleshooting

If Claude doesn't respond:
1. Check that the VM is running
2. Verify autonomous mode is disabled
3. Check the API endpoint is accessible
4. Look at the logs for errors

## Custom PR Tasks

You can send custom commands by modifying the templates in `trigger_pr_task.py` or sending direct commands via the API.