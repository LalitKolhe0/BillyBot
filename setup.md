# BillyBot React Frontend Setup



### ✨ Features Implemented

1. **Modern React UI** with Tailwind CSS
2. **PDF Upload Interface** with drag-and-drop functionality
3. **Chat Interface** for asking questions
4. **Settings Panel** for configuration
5. **FastAPI Backend** to handle requests
6. **Responsive Design** that works on all devices

### 📁 Project Structure

```
BillyBot/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── context/          # Settings context
│   │   ├── services/         # API client
│   │   └── App.js           # Main app
│   ├── package.json         # Dependencies
│   └── tailwind.config.js   # Tailwind config
├── backend/                  # FastAPI backend
│   ├── main.py             # API server
│   ├── vector_store.py     # Vector store logic
│   ├── chatbot.py          # Chat logic
│   └── requirements.txt    # Python dependencies
├── start.bat               # Windows startup script
└── README.md              # Documentation
```

### 🚀 Quick Start

1. **Install Ollama models**:
   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3
   ```

2. **Start the application**:
   - **Windows**: Double-click `start.bat`
   - **Manual**: 
     ```bash
     # Terminal 1 - Backend
     cd backend
     pip install -r requirements.txt
     python main.py
     
     # Terminal 2 - Frontend
     cd frontend
     npm install
     npm start
     ```

3. **Access the app**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### 🎨 UI Components

- **Header**: Clean app header with BillyBot branding
- **Settings Panel**: Configure models, chunk sizes, and retrieval parameters
- **File Upload**: Drag-and-drop PDF upload with progress indicators
- **Chat Interface**: Real-time chat with the AI assistant
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🔧 Configuration

The app includes a settings panel where you can adjust:
- Chroma database directory
- Ollama embedding model
- LLM model
- Chunk size and overlap
- Top-k retrieval count

### 📱 Modern Features

- **Loading States**: Spinners and progress indicators
- **Error Handling**: User-friendly error messages
- **File Management**: Preview and remove uploaded files
- **Chat History**: Persistent conversation history
- **Responsive Layout**: Adapts to different screen sizes

### 🛠️ Development

To customize or extend the frontend:

1. **Styling**: Modify `tailwind.config.js` for custom colors/themes
2. **Components**: Add new components in `src/components/`
3. **API**: Extend API client in `src/services/api.js`
4. **State**: Add new context providers in `src/context/`

The React frontend is now ready to use! It provides a modern, beautiful interface for your BillyBot Policy Chatbot with all the functionality of the original Streamlit app.
