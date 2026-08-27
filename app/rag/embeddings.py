import os

# 1. Empêche HuggingFace de tenter une connexion Internet
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """Charge et retourne le modèle d'embeddings en mode 100% hors-ligne."""
    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},  # Normalise les vecteurs pour une meilleure précision
    )
    return embeddings