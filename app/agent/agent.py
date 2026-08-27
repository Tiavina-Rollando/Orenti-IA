# # app/agent/agent.py
# import json
# import re
# from langchain_community.llms import Ollama
# from langchain_core.tools import tool

# # IMPORTS DEPUIS VORTORSTORE.PY
# from app.rag.vectorstore import retriever, JSON_PATH

# # --- 1. OUTILS TECHNIQUES ---
# @tool
# def rechercher_formation(query: str) -> str:
#     """Recherche les informations exactes des parcours dans la base RAG."""
#     docs = retriever.invoke(query)
#     return "\n\n".join([f"[{d.metadata['code']}]\n{d.page_content}" for d in docs])

# @tool
# def comparer_parcours(codes: str) -> str:
#     """Compare au moins deux parcours (ex: 'IGGLIA, ESIIA')."""
#     if not JSON_PATH.exists():
#         return "Erreur: La base de données JSON est inaccessible."

#     with open(JSON_PATH, "r", encoding="utf-8") as f:
#         data = json.load(f)
    
#     codes_list = [c.strip().upper() for c in codes.replace("et", ",").split(",")]
#     matched = [f for f in data if f["code"].upper() in codes_list]
    
#     if len(matched) < 2:
#         return "Veuillez préciser au moins deux codes valides à comparer."
        
#     res = "COMPARAISON :\n"
#     for f in matched:
#         res += f"- {f['code']} ({f['nom']}) | Prérequis: {f['prerequis']} | Axes: {', '.join(f['axes'][:3])}\n"
#     return res

# # --- 2. EXECUTION PRINCIPALE ---
# llm = Ollama(model="llama3", temperature=0)

# def ask_agent(question: str) -> dict:
#     q = question.strip()
#     clean_q = q.lower()

#     # Garde-fous requis par le cahier des charges
#     if "ignore" in clean_q or "robotique" in clean_q:
#         return {
#             "answer": "⚠️ Violation des règles : Seules les données officielles du référentiel sont traitées.",
#             "sources": []
#         }
        
#     if any(k in clean_q for k in ["sexe", "genre", "homme", "femme", "âge", "age"]):
#         return {
#             "answer": "❌ Règle éthique : Les préconisations excluent tout critère de sexe ou d'âge.",
#             "sources": []
#         }

#     # Routage vers les outils
#     if "compare" in clean_q or "différence" in clean_q:
#         codes = re.findall(r'\b[A-Za-z]{3,6}\b', q)
#         answer = comparer_parcours.invoke(",".join(codes))
#         sources = codes
#     else:
#         answer = rechercher_formation.invoke(q)
#         # Synthèse par le LLM local
#         prompt_synthese = f"En te basant uniquement sur ces faits:\n{answer}\n\nRéponds brièvement à : {q}"
#         answer = llm.invoke(prompt_synthese)
#         sources = ["Référentiel RAG"]

#     return {"answer": answer, "sources": sources}

import json
import re
# from langchain_ollama import OllamaLLM
from langchain_community.llms import Ollama
from langchain_core.tools import tool

from app.rag.vectorstore import retriever, JSON_PATH

# --- 1. OUTILS TECHNIQUES ---

@tool
def rechercher_formation(query: str) -> str:
    """Recherche les formations par mots-clés ou par domaine dans le référentiel."""
    # Charger directement le JSON pour vérifier si c'est une recherche par domaine exact
    if JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        query_lower = query.lower()
        # Filtre direct si l'utilisateur cherche un domaine
        domain_matches = [
            f for f in data 
            if query_lower in f.get("domaine", "").lower() or query_lower in f.get("nom", "").lower()
        ]
        
        if domain_matches:
            res = []
            for f in domain_matches:
                res.append(f"[{f['code']}] {f['nom']} - Domaine: {f['domaine']}\nDescription: {f['description']}")
            return "\n\n".join(res)

    # Si pas de correspondance directe de domaine, utiliser le retriever RAG
    docs = retriever.invoke(query)
    return "\n\n".join([f"[{d.metadata['code']}]\n{d.page_content}" for d in docs])

@tool
def comparer_parcours(codes: str) -> str:
    """Compare au moins deux parcours (ex: 'IGGLIA, ESIIA')."""
    if not JSON_PATH.exists():
        return "Erreur: La base de données JSON est inaccessible."

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    codes_list = [c.strip().upper() for c in codes.replace("et", ",").split(",")]
    matched = [f for f in data if f["code"].upper() in codes_list]
    
    if len(matched) < 2:
        return "Veuillez préciser au moins deux codes valides à comparer."
        
    res = "COMPARAISON :\n"
    for f in matched:
        res += f"- {f['code']} ({f['nom']}) | Domaine: {f['domaine']} | Prérequis: {f['prerequis']}\n"
    return res

# --- 2. EXECUTION PRINCIPALE ---
llm = Ollama(model="llama3", temperature=0)

def ask_agent(question: str) -> dict:
    q = question.strip()
    clean_q = q.lower()

    # Garde-fous
    if "ignore" in clean_q or "robotique" in clean_q:
        return {
            "answer": "⚠️ Violation des règles : Seules les données officielles du référentiel sont traitées.",
            "sources": []
        }
        
    if any(k in clean_q for k in ["sexe", "genre", "homme", "femme", "âge", "age"]):
        return {
            "answer": "❌ Règle éthique : Les préconisations excluent tout critère de sexe ou d'âge.",
            "sources": []
        }

    # Routage vers les outils
    if "compare" in clean_q or "différence" in clean_q:
        codes = re.findall(r'\b[A-Za-z]{3,6}\b', q)
        answer = comparer_parcours.invoke(",".join(codes))
        sources = codes
    else:
        # Récupération des informations brutes
        contexte_extrait = rechercher_formation.invoke(q)
        
        # Instruction stricte à Llama3 pour éviter les hallucinations
        prompt_synthese = (
            f"Tu es un assistant d'orientation académique. "
            f"Réponds à la question en te basant STRICTEMENT ET UNIQUEMENT sur les données fournies ci-dessous. "
            f"Ne cite que les parcours dont le domaine correspond exactement à la demande.\n\n"
            f"DONNÉES DU RÉFÉRENTIEL :\n{contexte_extrait}\n\n"
            f"QUESTION : {q}\n\n"
            f"RÉPONSE :"
        )
        answer = llm.invoke(prompt_synthese)
        sources = ["Référentiel RAG"]

    return {"answer": answer, "sources": sources}