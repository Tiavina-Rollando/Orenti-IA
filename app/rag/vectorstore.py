# app/rag/vectorstore.py
import os
import json
from pathlib import Path

# Fix hors-ligne
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# ROOT_DIR pointe vers la racine du projet (Orenti'IA)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
JSON_PATH = ROOT_DIR / "data" / "formations.json"
CHROMA_DIR = ROOT_DIR / "chroma_db"

def init_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    if os.path.exists(CHROMA_DIR):
        return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)

    if not JSON_PATH.exists():
        raise FileNotFoundError(f"Fichier introuvable à l'emplacement : {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for f in data:
        content = (
            f"Code: {f['code']}\nNom: {f['nom']}\nDomaine: {f['domaine']}\n"
            f"Description: {f['description']}\nAxes: {', '.join(f['axes'])}\n"
            f"Compétences: {', '.join(f['competences'])}\nDébouchés: {', '.join(f['debouches'])}\n"
            f"Prérequis: {f['prerequis']}\nConcours: {', '.join(f['concours'])}"
        )
        docs.append(Document(page_content=content, metadata={"code": f['code']}))

    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

# Instance unique du retriever et constante exportée
vectorstore = init_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})