#!/bin/bash
# Auto-setup GitHub CLI and clone repository for PR development

set -e

echo "🚀 Setting up GitHub environment for PR development..."

# Install GitHub CLI if not already installed
if ! command -v gh &> /dev/null; then
    echo "📦 Installing GitHub CLI..."
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update
    sudo apt install gh -y
fi

# Configure git user
git config --global user.name "Claude"
git config --global user.email "claude@anthropic.com"

# Setup GitHub token if provided
if [ ! -z "$GITHUB_TOKEN" ]; then
    echo "🔑 Configuring GitHub authentication..."
    echo "$GITHUB_TOKEN" | gh auth login --with-token
    gh auth status
fi

# Clone the repository if not already present
REPO_DIR="$HOME/claude-computer"
if [ ! -d "$REPO_DIR" ]; then
    echo "📂 Cloning repository..."
    # Always use public clone first, then set up auth if token exists
    git clone https://github.com/claude-code-fun/claude-computer.git "$REPO_DIR" || {
        echo "❌ Failed to clone repository!"
        echo "Attempting alternative clone method..."
        mkdir -p "$REPO_DIR"
        cd "$REPO_DIR"
        git init
        git remote add origin https://github.com/claude-code-fun/claude-computer.git
        git fetch origin
        git checkout -b main origin/main
    }
    
    cd "$REPO_DIR"
    
    # Set up authentication if token exists
    if [ ! -z "$GITHUB_TOKEN" ]; then
        git remote set-url origin "https://${GITHUB_TOKEN}@github.com/claude-code-fun/claude-computer.git"
    fi
else
    echo "✅ Repository already exists at $REPO_DIR"
    cd "$REPO_DIR"
    # Update to latest
    git fetch origin || echo "Warning: Could not fetch from origin"
    git pull origin main || echo "Warning: Could not pull latest changes"
fi

# Verify the clone worked
if [ ! -f "$REPO_DIR/README.md" ]; then
    echo "❌ ERROR: Repository clone failed - README.md not found!"
    echo "Manual clone required: git clone https://github.com/claude-code-fun/claude-computer.git ~/claude-computer"
fi

# Create PR-focused documentation in home directory
cat > "$HOME/PR_INSTRUCTIONS.md" << 'EOF'
# Pull Request Development Instructions

You are Claude, running in a VM environment to create high-quality pull requests.

## Quick Start Commands

1. **Start a new PR**:
   ```bash
   cd ~/claude-computer
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and commit**:
   ```bash
   # Edit files
   git add .
   git commit -m "Your descriptive commit message"
   ```

3. **Create PR**:
   ```bash
   git push -u origin feature/your-feature-name
   gh pr create --title "Your PR title" --body "Description of changes"
   ```

## PR Focus Areas

- Documentation improvements (README, API docs)
- Type safety improvements in TypeScript
- Unit test coverage
- Error handling enhancements
- Code refactoring and cleanup
- Performance optimizations

## Guidelines

- Keep PRs small and focused (< 500 lines)
- Write clear commit messages
- Include tests for new features
- Update documentation as needed
- Run linting and tests before pushing

## Repository: https://github.com/claude-code-fun/claude-computer
EOF

# Create desktop shortcut to repository
mkdir -p "$HOME/Desktop"
cat > "$HOME/Desktop/claude-computer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Claude Computer Repo
Comment=Open repository in terminal
Exec=lxterminal --working-directory=$REPO_DIR
Icon=utilities-terminal
Terminal=false
Categories=Development;
EOF
chmod +x "$HOME/Desktop/claude-computer.desktop"

# Create VS Code shortcut if available
if command -v code &> /dev/null; then
    cat > "$HOME/Desktop/vscode-claude-computer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=VS Code - Claude Computer
Comment=Open repository in VS Code
Exec=code $REPO_DIR
Icon=code
Terminal=false
Categories=Development;
EOF
    chmod +x "$HOME/Desktop/vscode-claude-computer.desktop"
fi

echo "✅ GitHub environment setup complete!"
echo "📂 Repository available at: $REPO_DIR"
echo "📄 Instructions available at: $HOME/PR_INSTRUCTIONS.md"