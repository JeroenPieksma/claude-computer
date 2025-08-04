# Claude Computer 🤖

<div align="center">
  <img src="https://img.shields.io/badge/Claude-Autonomous-blue" alt="Claude Autonomous" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" />
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome" />
  <img src="https://img.shields.io/badge/$CCF-Rewards-purple" alt="$CCF Rewards" />
</div>

<div align="center">
  <h3>An open-source platform showcasing Claude's autonomous computer interaction capabilities</h3>
  <p>Watch Claude navigate, research, create, and explore in real-time</p>
  <p><a href="https://www.autonomous.claudecode.fun/">🌐 Live Demo</a></p>
</div>

## 🎯 Overview

Claude Computer is an innovative demonstration of AI autonomy, allowing Claude to operate independently in a virtual machine environment. The system combines real-time streaming, behavioral frameworks, and audience interaction to showcase advanced AI capabilities in action.

## 💰 Contributor Rewards - $CCF Token

We believe in rewarding our contributors! Active contributors can earn **$CCF tokens** for their efforts.

- **Token Contract**: `J8DWsKbZyLQXrzxMsF5TbLy5f3uHTC8jTbhtkUGwbonk` (Solana)
- **Learn More**: [autonomous.claudecode.fun](https://www.autonomous.claudecode.fun/)
- **How to Earn**: See [CONTRIBUTING.md](CONTRIBUTING.md) for details on earning $CCF

### Reward Categories:
- 🐛 **Bug Fixes**: 100-500 $CCF
- ✨ **New Features**: 500-2000 $CCF
- 📚 **Documentation**: 50-200 $CCF
- 🎨 **UI/UX Improvements**: 200-1000 $CCF
- 🚀 **Performance Optimizations**: 300-1500 $CCF

## 🏗️ Architecture

```
┌─────────────────┬─────────────────┬─────────────────┐
│   Frontend      │    Backend      │  VM Environment │
│   (Next.js)     │   (FastAPI)     │   (Docker)      │
├─────────────────┼─────────────────┼─────────────────┤
│ • React/TS      │ • WebSocket     │ • Ubuntu Desktop│
│ • Real-time UI  │ • Claude Agent  │ • VNC Access    │
│ • Multi-view    │ • Behaviors     │ • Tool Access   │
└─────────────────┴─────────────────┴─────────────────┘
```

## ✨ Features

- 🖥️ **Real-time Desktop Streaming** - Watch Claude's screen in real-time
- 🤖 **20+ Autonomous Behaviors** - Research, create, explore, and more
- 💬 **Live Commentary** - AI-generated insights and reactions
- 📊 **Activity Timeline** - Track and analyze Claude's actions
- 🎯 **Task Management** - Direct Claude with specific objectives
- 🔄 **State Persistence** - VM state saved across sessions
- 🛡️ **Safety First** - Isolated VM environment with monitoring

## 🚀 Quick Start

```bash
# Start the VM environment
./scripts/start-vm.sh

# Launch backend server
cd backend && python -m uvicorn main:app --reload

# Start frontend
cd frontend && npm run dev
```

## 🛠️ Development Setup

### Prerequisites
- Docker Desktop
- Python 3.11+
- Node.js 18+
- Anthropic API key
- Supabase account (for database)

### Environment Variables
```bash
ANTHROPIC_API_KEY=your_anthropic_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

### Database Setup
- **Schema Documentation**: See [docs/DATABASE.md](docs/DATABASE.md) for complete database structure
- **TypeScript Types**: Database types available in `frontend/types/database.ts`
- **Supabase Project**: Create tables using the SQL migrations in the documentation

### Local Development
```bash
# Clone the repository
git clone https://github.com/claude-code-fun/claude-computer.git
cd claude-computer

# Run setup script
./scripts/dev-setup.sh

# Start everything
./scripts/start-vm.sh
```

## 📡 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **VNC Desktop**: http://localhost:6080/vnc.html

## 🤝 Contributing

We welcome contributions from developers worldwide! Please see our [Contributing Guide](CONTRIBUTING.md) for:
- How to get started
- Code standards and review process
- $CCF token reward details
- Priority areas for contribution

## 📋 Current Priorities

- [ ] Fix various bugs and stability issues
- [ ] Fix async issue causing container crashes from too many concurrent operations
- [ ] Fix memory generation logic and persistence
- [ ] Improve streaming performance and reliability
- [ ] Enable simultaneous autonomous mode + chat/command mode
- [ ] Enhanced memory system implementation
- [ ] Multi-modal interaction capabilities
- [ ] Advanced behavioral patterns
- [ ] Performance optimizations
- [ ] Mobile responsive UI
- [ ] Additional language support

## 🏆 Top Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- This section will be automatically updated -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Website**: [autonomous.claudecode.fun](https://www.autonomous.claudecode.fun/)
- **$CCF Token**: `J8DWsKbZyLQXrzxMsF5TbLy5f3uHTC8jTbhtkUGwbonk`
- **Twitter/X**: [@Claude_Code_fun](https://x.com/Claude_Code_fun)
- **Discord**: Coming soon!

## 🙏 Acknowledgments

- Built on [Anthropic's Computer Use Demo](https://github.com/anthropics/anthropic-quickstarts)
- Powered by Claude (Anthropic)
- Community-driven development

---

<div align="center">
  <p>Made with ❤️ by the Claude Computer community</p>
  <p>Earn $CCF tokens by contributing!</p>
</div>
