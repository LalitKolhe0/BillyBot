# HR Policy Chatbot

Small Streamlit app that ingests HR policy documents (PDF/MD/TXT), embeds them into a local vector store (Chroma or FAISS), and answers employee HR questions using a local or cloud LLM via LangChain.

This README covers: quick setup, running the app, common errors (including the `unstructured` error you hit), tests, and where important files live.

## Quick setup (Windows / PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies (recommended: from the project `requirements.txt`). Update the file if you need additional packages listed below.

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

If you prefer to install individual packages (useful if you customize vector stores or loaders):

```powershell
.\venv\Scripts\python.exe -m pip install langchain langchain-community streamlit chromadb faiss-cpu python-dotenv pypdf python-docx sentence-transformers huggingface-hub
# Required by the Unstructured markdown/pdf loaders used by langchain_community
.\venv\Scripts\python.exe -m pip install "unstructured[all-docs]"  # recommended when using UnstructuredMarkdownLoader / UnstructuredPDFLoader
```


3. Start any model server you use (optional):

- If you use Ollama: `ollama serve` and `ollama pull <model>`
- If you use Hugging Face Inference: ensure `HUGGINGFACEHUB_API_TOKEN` or the token environment variable you use is set.

4. Run the Streamlit app:

```powershell
.\venv\Scripts\python.exe -m streamlit run app/streamlit_app.py --server.headless true
```


## Project layout (key files)

- `app/streamlit_app.py` — Streamlit UI and app entrypoint.
- `app/` — Streamlit app package and configuration.
- `src/document_processor.py` — document loaders and text splitter logic.
- `src/vector_store.py` — vector DB manager (Chroma or FAISS) and embeddings setup.
- `src/chatbot.py` — chat wrapper that calls the LLM.
- `data/` — place to add HR documents (ignored by git by default).
- `.streamlit/config.toml` — Streamlit theme (dark) and server settings.
- `.vscode/settings.json` — workspace settings (theme: Default Dark+).


## Common error: ModuleNotFoundError: No module named 'unstructured'

Symptoms:
- Traceback shows `ModuleNotFoundError: No module named 'unstructured'` coming from `langchain_community.document_loaders`.

Cause:
- `UnstructuredMarkdownLoader` and other loaders require the `unstructured` package and its optional extras. `langchain_community` checks for a minimum `unstructured` version and raises if missing.

Fix:

```powershell
.\venv\Scripts\python.exe -m pip install "unstructured[all-docs]"
# Or at minimum:
.\venv\Scripts\python.exe -m pip install "unstructured>=0.4.16"
```

After installing re-run Streamlit (see Run command above). If you still see errors about `unstructured` version, upgrade it:

```powershell
.\venv\Scripts\python.exe -m pip install -U "unstructured[all-docs]"
```


## Troubleshooting other common issues

- Missing OpenAI / Hugging Face keys: set `OPENAI_API_KEY` or `HUGGINGFACEHUB_API_TOKEN` (or whichever variable the app expects) in your environment or `.env` file in project root.
- LangChain deprecation warnings: they are warnings; the app should still run. To remove them, update imports per the latest LangChain docs or use `langchain-community` counterparts.
- Chromadb persistence errors: some Chroma wrappers don't expose `.persist()` — `src/vector_store.py` already ignores errors when persistence is not available.


## Tests

Run tests with pytest:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```


## VS Code notes

- Workspace theme: `Default Dark+` is set in `.vscode/settings.json`.
- There are tasks in `.vscode/tasks.json` for running tests and running the app using the venv.


## Recommended next steps

- If you plan to run locally with complex PDFs, install `unstructured[all-docs]` as above.
- Pin exact dependency versions in `requirements.txt` so installs are reproducible.
- If you want, I can update `requirements.txt` for you and run `pip install -r requirements.txt` in the venv to verify everything installs.


## License

MIT — see `LICENSE`.


## Future 
1. Option for selecting models or LLMs hrough API integration
2. Identity aceess management  - User Role defination
3.  Settings or Configuration pages for this
4. VectorDB from cloud
5. Folder to upload docs. (Or List of docs uploaded can be seen )
6. UI in REACT
7. 



