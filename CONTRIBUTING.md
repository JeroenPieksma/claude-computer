# Contributing to Claude Computer

Thank you for your interest in contributing to Claude Computer! We're excited to have you join our community and help build the future of autonomous AI demonstrations.

## 💰 $CCF Token Rewards

We reward contributors with $CCF tokens for their valuable contributions!

### Token Details
- **Contract Address**: `J8DWsKbZyLQXrzxMsF5TbLy5f3uHTC8jTbhtkUGwbonk` (Solana)
- **Website**: [autonomous.claudecode.fun](https://www.autonomous.claudecode.fun/)

### Reward Structure

| Contribution Type | Reward Range | Examples |
|------------------|--------------|----------|
| 🐛 Bug Fixes | 20,000-100,000 $CCF | Fixing crashes, resolving errors, patching security issues |
| ✨ New Features | 100,000-400,000 $CCF | New behaviors, UI components, API endpoints |
| 📚 Documentation | 10,000-40,000 $CCF | README updates, API docs, tutorials |
| 🎨 UI/UX | 40,000-200,000 $CCF | Design improvements, responsive layouts, animations |
| 🚀 Performance | 60,000-300,000 $CCF | Speed optimizations, memory improvements, caching |
| 🧪 Testing | 20,000-80,000 $CCF | Unit tests, integration tests, E2E tests |
| 🌐 Translations | 20,000-60,000 $CCF | Internationalizing the application |

*Rewards subject to change based on $CCF token price*

### How to Claim Rewards
1. Make your contribution via pull request
2. Once merged, comment on the PR with your Solana wallet address
3. Rewards are distributed weekly
4. Join our Discord (coming soon) for updates

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/claude-computer.git
cd claude-computer
```

### 2. Set Up Development Environment
```bash
# Run the setup script
./scripts/dev-setup.sh

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📋 Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 standards
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

```python
async def process_message(message: str, user_id: str) -> dict:
    """Process incoming WebSocket message.
    
    Args:
        message: The message content
        user_id: Unique identifier for the user
        
    Returns:
        Dictionary with response data
    """
    # Implementation
```

#### TypeScript/React (Frontend)
- Use functional components with TypeScript
- Implement proper error boundaries
- Use React hooks appropriately
- Follow naming conventions

```typescript
interface ComponentProps {
  title: string;
  onAction: (id: string) => void;
}

const MyComponent: React.FC<ComponentProps> = ({ title, onAction }) => {
  // Implementation
};
```

### Commit Messages
Follow conventional commits format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Test additions/changes
- `chore:` Build process/auxiliary changes

Example: `feat: add voice interaction capability to chat interface`

## 🔄 Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass
   - Update documentation if needed
   - Test your changes thoroughly
   - Add yourself to contributors list

2. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] Tested locally
   - [ ] Added/updated tests
   - [ ] All tests pass
   
   ## Wallet for Rewards
   SOL Address: YOUR_WALLET_ADDRESS
   ```

3. **Review Process**
   - Automated checks must pass
   - Code review by maintainers
   - Address feedback promptly
   - Once approved, it will be merged

## 🎯 Priority Areas

### High Priority 🔴
- Memory system implementation
- WebRTC video streaming
- Mobile responsive design
- Authentication system
- Real-time collaboration features

### Medium Priority 🟡
- Additional behavioral patterns
- Internationalization
- Advanced analytics dashboard
- Plugin system architecture
- Voice interaction

### Good First Issues 🟢
- UI component improvements
- Documentation updates
- Bug fixes in activity logger
- Adding unit tests
- Accessibility improvements

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
npm run test:e2e
```

### Writing Tests
- Aim for 80%+ code coverage
- Test edge cases
- Include integration tests for new features
- Document test purposes

## 📚 Documentation

### Where to Document
- **Code**: Inline comments and docstrings
- **API**: Update OpenAPI specs
- **Features**: Update README.md
- **Architecture**: Update CLAUDE.md
- **Guides**: Create in `/docs` folder

### Documentation Standards
- Clear and concise
- Include code examples
- Explain the "why" not just "what"
- Keep it up to date

## 🤝 Community

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussions and Q&A
- **Discord**: Coming soon!
- **Twitter**: Coming soon!

### Code of Conduct
Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

### Getting Help
- Check existing issues and discussions
- Read the documentation thoroughly
- Ask in GitHub Discussions
- Be patient and respectful

## 🔐 Security

### Reporting Security Issues
Please DO NOT open public issues for security vulnerabilities. Instead:
1. Email security@claudecode.fun (coming soon)
2. Or DM maintainers directly
3. We'll respond within 48 hours

### Security Best Practices
- Never commit API keys or secrets
- Validate all user inputs
- Use parameterized queries
- Keep dependencies updated
- Follow OWASP guidelines

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be:
- Listed in our README
- Eligible for $CCF token rewards
- Invited to exclusive contributor events
- Given special roles in our Discord

---

**Thank you for contributing to Claude Computer! Together, we're building the future of autonomous AI.** 🚀

*Questions? Open an issue or reach out to the maintainers.*