# 🚀 Quick Start Guide - 5 Minutes to BillyBot

Get BillyBot up and running in 5 minutes!

## Prerequisites Check

```bash
# Check Python (need 3.8+)
python --version

# Check Node.js (need 16+) - Optional, only for React interface
node --version

# Check Ollama
ollama --version
```

Don't have something? Install:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Ollama: https://ollama.ai

---

## 🎯 Choose Your Path

### Path A: Streamlit (Easiest - 2 Minutes)

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt

# 2. Install Ollama models (this takes 2-3 minutes)
ollama pull nomic-embed-text
ollama pull llama3

# 3. Run it!
streamlit run streamlit_app.py

# ✅ Open http://localhost:8501
```

**That's it!** You're done. Skip to [First Use](#-first-use) below.

---

### Path B: React Interface (5 Minutes)

```bash
# 1. Backend setup
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Install Ollama models
ollama pull nomic-embed-text
ollama pull llama3

# 3. Frontend setup
cd ../frontend
npm install
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# 4. Run backend (keep this terminal open)
cd ../backend
python main.py

# 5. Run frontend (open NEW terminal)
cd frontend
npm start

# ✅ Opens automatically at http://localhost:3000
```

---

## 📝 First Use

### 1. Upload a PDF

**Streamlit:**
- Go to "Upload PDFs" tab
- Click "Choose PDF files"
- Select your PDF
- Click "Ingest PDFs into Chroma"

**React:**
- Stay on "Upload PDFs" tab
- Drag & drop PDF or click to browse
- Click "Upload Files"

### 2. Ask a Question

**Streamlit:**
- Go to "Ask Questions" tab
- Type your question
- Click "Ask Question"

**React:**
- Click "Ask Questions" tab
- Type your question
- Click "Ask" or press Enter

### 3. View Answer

Your answer appears with source citations!

---

## 🎨 Customize Settings

### Streamlit
Adjust in the left sidebar:
- Change models
- Adjust chunk sizes
- Modify retrieval count (Top-K)

### React
Click the ⚙️ settings panel on the left

---

## ⚡ Quick Commands Reference

### Stop Everything
```bash
# Kill all processes
Ctrl+C (in each terminal)
```

### Restart

**Streamlit:**
```bash
streamlit run streamlit_app.py
```

**React:**
```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
cd frontend && npm start
```

### Clear Database
- **Streamlit:** Go to "Database Management" tab → Type "DELETE" → Click button
- **React:** Click "Clear DB" button → Confirm

---

## ❓ Common Quick Fixes

### "Module not found" error
```bash
pip install -r backend/requirements.txt
```

### "Ollama connection refused"
```bash
ollama serve
```

### "Port already in use"
```bash
# Kill the process
lsof -ti:8000 | xargs kill -9   # Backend
lsof -ti:3000 | xargs kill -9   # Frontend
```

### Frontend won't connect to backend
```bash
# Check .env file exists
cat frontend/.env
# Should show: REACT_APP_API_URL=http://localhost:8000
```

---

## 🎓 Next Steps

Now that it's working:

1. **Read the full README** - Understand the architecture
2. **Try different models** - `ollama pull mistral` then change in settings
3. **Adjust parameters** - Experiment with chunk sizes and Top-K
4. **Upload multiple PDFs** - Build a knowledge base
5. **Check API docs** - Visit http://localhost:8000/docs

---

## 📚 Learn More

- Full README: [README.md](README.md)
- Detailed Installation: [INSTALLATION.md](docs/INSTALLATION.md)
- API Documentation: http://localhost:8000/docs
- Troubleshooting: See README.md § Troubleshooting

---

## 🆘 Need Help?

1. Check if Ollama is running: `ollama list`
2. Check if backend is running: `curl http://localhost:8000/health`
3. Read error messages carefully
4. Open an issue on GitHub

---

**🎉 Congratulations!** You're now running BillyBot. Happy chatting!