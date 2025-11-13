# vector_store.py
import os
from typing import List
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil
import tempfile
import json



class VectorStoreManager:
    def __init__(
        self,
        persist_directory: str = "chroma_kb_db",
        embedding_model: str = "nomic-embed-text",  # make sure you pulled this with ollama
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        collection_name: str = "kb_documents",
    ):
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Ollama embeddings
        self.embeddings = OllamaEmbeddings(model=self.embedding_model)

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def ingest_pdfs(self, pdf_paths: List[str], overwrite: bool = False):
        if overwrite and os.path.exists (self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)

        docs = []
        for pdf_path in pdf_paths:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            splits = self.splitter.split_documents(pages)
            for s in splits:
                s.metadata = s.metadata or {}
                s.metadata["source"] = Path(pdf_path).name
            docs.extend(splits)

        if not docs:
            raise ValueError("No documents found to ingest.")

        chroma_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
        )
        try:
            chroma_db.persist()
        except Exception:
            pass

        return chroma_db

    def load_chroma(self):
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )

    def get_relevant(self, query: str, k: int = 4):
        db = self.load_chroma()
        return db.similarity_search(query, k=k)


    def clear_database(self):
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            return {"message": "Knowledge base cleared successfully"}
        else:
            return {"message": "No database found to clear"}
