import json
from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.documents import Document
from rag.embeddings import get_embedding_model

# Définition des chemins
BASE_DIR = Path(__file__).resolve().parent.parent.parent
JSON_PATH = BASE_DIR / "data" / "formations.json"
DB_DIR = BASE_DIR / "data" / "chroma_db"


def build_or_get_vector_store():
    """Crée le Vector Store s'il n'existe pas, sinon le charge depuis le disque."""
    embeddings = get_embedding_model()

    # Si la base de données existe déjà sur le disque, on la charge
    if DB_DIR.exists():
        return Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=embeddings,
        )

    # Sinon, on lit le JSON et on crée la base vectorielle
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"Fichier introuvable : {JSON_PATH}")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        formations = json.load(f)

    documents = []
    for f in formations:
        # Formatage structuré accentuant le Domaine Principal pour le RAG
        content = f"""
Formation: {f.get('nom', '')} ({f.get('code', '')})
Domaine : {f.get('domaine', '')}
Description: {f.get('description', '')}
Axes d'étude: {', '.join(f.get('axes', []))}
Compétences acquises: {', '.join(f.get('competences', []))}
Débouchés / Métiers: {', '.join(f.get('debouches', []))}
Prérequis: {f.get('prerequis', '')}
Concours: {', '.join(f.get('concours', []))}
        """.strip()

        # Métadonnées enrichies pour faciliter le filtrage UI et le débogage
        metadata = {
            "code": f.get("code", ""),
            "nom": f.get("nom", ""),
            "domaine": f.get("domaine", ""),
        }

        documents.append(Document(page_content=content, metadata=metadata))

    # Génération et sauvegarde du Vector Store
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
    )
    return vector_store