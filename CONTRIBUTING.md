# Contributing to BillyBot

Thank you for your interest in contributing to BillyBot! 🎉

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Docker and Docker Compose
- Git

### Development Setup

1. **Fork and clone** the repository:
   ```bash
   git clone https://github.com/yourusername/billybot.git
   cd billybot
   ```

2. **Install dependencies**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

3. **Start development servers**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   python main.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

## 🛠️ Development Guidelines

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **JavaScript/React**: Use Prettier, follow ESLint rules
- **Commits**: Use conventional commit messages

### Testing

- **Backend**: Add tests in `backend/tests/`
- **Frontend**: Add tests in `frontend/src/__tests__/`
- **Run tests**: `npm test` and `pytest`

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test thoroughly

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** with:
   - Clear description of changes
   - Screenshots (if UI changes)
   - Test results

## 📝 Issue Guidelines

### Bug Reports

Include:
- **Environment**: OS, Python/Node versions
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots/logs**

### Feature Requests

Include:
- **Use case description**
- **Proposed solution**
- **Alternatives considered**

## 🏗️ Architecture

### Frontend (React)
- **Components**: Reusable UI components
- **Context**: State management
- **Services**: API communication
- **Styling**: Tailwind CSS

### Backend (FastAPI)
- **API**: RESTful endpoints
- **Vector Store**: Chroma integration
- **AI**: Ollama integration
- **Processing**: PDF handling

## 🐳 Docker Development

```bash
# Build and run with Docker
docker-compose up --build

# Run tests in Docker
docker-compose exec billybot python -m pytest
```

## 📚 Documentation

- **API**: Documented with FastAPI auto-docs
- **Components**: JSDoc comments
- **README**: Keep updated with changes

## 🤝 Community

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Report bugs and request features
- **Code Review**: All PRs require review

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to BillyBot! 🚀
