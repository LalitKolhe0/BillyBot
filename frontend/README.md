# BillyBot Frontend

Modern React frontend for the BillyBot Policy Chatbot.

## Features

- 🎨 Beautiful, responsive UI with Tailwind CSS
- 📄 Drag-and-drop PDF upload
- 💬 Real-time chat interface
- ⚙️ Configurable settings panel
- 🔄 Loading states and error handling

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on http://localhost:8000

### Installation

```bash
npm install
npm start
```

The app will open at http://localhost:3000

### Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:8000
```

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## Project Structure

```
src/
├── components/          # React components
│   ├── Header.js       # App header
│   ├── SettingsPanel.js # Settings sidebar
│   ├── FileUpload.js   # PDF upload component
│   └── ChatInterface.js # Chat interface
├── context/            # React context
│   └── SettingsContext.js # Settings state management
├── services/           # API services
│   └── api.js         # API client
├── App.js             # Main app component
├── index.js           # App entry point
└── index.css          # Global styles
```

## Technologies Used

- React 18
- Tailwind CSS
- Lucide React (icons)
- Axios (HTTP client)
- React Dropzone (file upload)
