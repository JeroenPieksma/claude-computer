#!/bin/bash

# Script to create bounty-related labels on GitHub
# Usage: ./scripts/setup-bounty-labels.sh

echo "🏷️  Setting up bounty labels for Claude Computer..."

# Function to create a label
create_label() {
    local name=$1
    local color=$2
    local description=$3
    
    echo "Creating label: $name"
    curl -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/repos/claude-code-fun/claude-computer/labels \
        -d "{\"name\":\"$name\",\"color\":\"$color\",\"description\":\"$description\"}"
    echo ""
}

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable is not set"
    echo "Please set it with: export GITHUB_TOKEN=your_github_pat"
    exit 1
fi

# Create bounty-related labels
create_label "bounty" "FFD700" "Task with $CCF token reward"
create_label "bounty-claimed" "FFA500" "Bounty has been claimed by someone"
create_label "bounty-easy" "7CFC00" "Good first bounty (20k-100k $CCF)"
create_label "bounty-medium" "FFD700" "Medium difficulty bounty (50k-200k $CCF)"
create_label "bounty-hard" "FF6347" "Hard bounty (100k-400k $CCF)"
create_label "bounty-critical" "DC143C" "Critical priority bounty (200k-600k $CCF)"

echo "✅ Bounty labels created successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Create bounty issues using the bounty template"
echo "2. Add appropriate bounty difficulty labels"
echo "3. Share the bounties board link with the community"