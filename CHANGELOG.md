# Changelog

All notable changes to BillyBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- User authentication and authorization
- Support for DOCX and TXT files
- Chat history persistence in database
- Export conversations to PDF/Markdown
- Docker deployment configuration
- Batch question processing
- Advanced search filters

---

## [0.1.0] - 2024-01-XX

### Added
- 🎉 Initial release of BillyBot
- 📄 PDF document upload and processing
- 🔍 Semantic search using ChromaDB vector store
- 💬 Question-answering with Ollama LLM
- ⚛️ React frontend with modern UI
- 🎨 Streamlit alternative interface
- ⚙️ Configurable settings (models, chunk sizes, retrieval parameters)
- 🗄️ Persistent vector storage with ChromaDB
- 🔄 Real-time processing feedback
- 🧹 Database management (clear/reset)
- 📊 Source citations in answers
- 🎯 Drag-and-drop file upload (React)
- 💾 Chat history (Streamlit)
- 📚 Comprehensive documentation
- 🚀 FastAPI backend with async support
- 🔌 RESTful API with Swagger documentation

### Backend
- FastAPI application with CORS support
- Vector store manager with LangChain integration
- ChromaDB for vector embeddings storage
- Ollama integration for embeddings and LLM
- PDF processing with PyPDF
- Text chunking with configurable parameters
- Semantic search and retrieval
- Health check and status endpoints

### Frontend (React)
- Modern responsive UI with Tailwind CSS
- Settings panel with real-time updates
- File upload component with drag-and-drop
- Chat interface with message history
- Error handling and loading states
- API integration with Axios
- Environment variable configuration

### Frontend (Streamlit)
- Three-tab interface (Upload, Chat, Database)
- Built-in chat history
- Real-time settings updates
- Database size monitoring
- Safe database deletion with confirmation
- Custom CSS styling
- Temporary file cleanup

### Dependencies
- Python 3.8+ support
- Node.js 16+ support
- FastAPI 0.104.1
- LangChain 0.1.0
- ChromaDB 0.4.18
- Ollama 0.1.7
- React 18.2
- Streamlit 1.28.0

### Documentation
- Comprehensive README.md
- Quick start guide
- Detailed installation instructions
- API documentation
- Troubleshooting guide
- Contributing guidelines
- License (MIT)

### Fixed
- Removed authentication requirements (simplified for initial release)
- Fixed CORS configuration for frontend connection
- Resolved endpoint naming inconsistencies
- Fixed import path issues in Streamlit
- Corrected database clearing functionality
- Fixed temporary file cleanup after upload

### Security
- Local-only operation (no external API keys required)
- No authentication in initial release (planned for future)
- Environment variable support for sensitive configuration

---

## Version Numbering

BillyBot follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for backwards compatible bug fixes

Example: `v1.2.3` means:
- `1` = Major version
- `2` = Minor version  
- `3` = Patch version

---

## Release Types

### 🎉 Major Release (x.0.0)
- Breaking changes
- Major new features
- Architecture changes

### ✨ Minor Release (0.x.0)
- New features
- Enhancements
- Non-breaking changes

### 🐛 Patch Release (0.0.x)
- Bug fixes
- Security patches
- Minor improvements

---

## Migration Guides

### From v0.1.0 to v0.2.0 (when released)
*Migration guide will be added when v0.2.0 is released*

---

