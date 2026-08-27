from typing import Dict, List
from app.rag.vector_store import build_or_get_vector_store


def get_relevant_documents(
    query: str, top_k: int = 10, score_threshold: float = 0.3
) -> List[Dict]:
    """Recherche les formations pertinentes avec un filtrage par score de similarité.

    - top_k: Nombre maximum de formations à retourner (ex: 10 au lieu de 3)
    - score_threshold: Seuil minimum de pertinence (entre 0 et 1)
    """
    vector_store = build_or_get_vector_store()

    # Recherche avec retour des scores de similarité
    results_with_scores = (
        vector_store.similarity_search_with_relevance_scores(
            query, k=top_k
        )
    )

    relevant_results = []
    for doc, score in results_with_scores:
        # On ne garde que les formations dont le score dépasse le seuil minimal
        if score >= score_threshold:
            relevant_results.append(
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": round(score, 3),
                }
            )

    # Si aucune formation ne dépasse le seuil, on renvoie au moins la plus proche
    if not relevant_results and results_with_scores:
        doc, score = results_with_scores[0]
        relevant_results.append(
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": round(score, 3),
            }
        )

    return relevant_results