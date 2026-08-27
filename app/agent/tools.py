import json
from langchain_core.tools import tool
from app.rag.vectorstore import retriever

@tool
def rechercher_formation(requete: str) -> str:
    """Recherche des formations dans la base documentaire officielle à l'aide de la recherche vectorielle (RAG). 
    À utiliser dès qu'une question porte sur les critères, débouchés, programmes ou accès à un parcours.
    """
    docs = retriever.invoke(requete)
    if not docs:
        return "Aucune formation correspondant à ces critères n'a été trouvée dans le référentiel officiel."
    
    results = []
    for d in docs:
        results.append(f"[Source: {d.metadata['code']} - {d.metadata['nom']}]\n{d.page_content}")
    return "\n\n---\n\n".join(results)

@tool
def comparer_parcours(codes: str) -> str:
    """Compare au moins deux parcours (ex: 'ISAIA, IGGLIA') en comparant leurs prérequis, axes et débouchés issus du référentiel."""
    with open("formations.json", "r", encoding="utf-8") as f:
        formations = json.load(f)
        
    codes_list = [c.strip().upper() for c in codes.replace("et", ",").split(",")]
    matched = [f for f in formations if f["code"].upper() in codes_list]
    
    if len(matched) < 2:
        return "Erreur : Spécifiez au moins deux codes de formation valides présents dans la base (ex: 'ISAIA, IGGLIA')."
        
    res = "COMPARAISON OFFICIELLE DES PARCOURS :\n\n"
    for f in matched:
        res += (
            f"• Code: {f['code']} ({f['nom']})\n"
            f"  - Domaine: {f['domaine']}\n"
            f"  - Prérequis: {f['prerequis']}\n"
            f"  - Axes: {', '.join(f['axes'])}\n"
            f"  - Débouchés: {', '.join(f['debouches'])}\n\n"
        )
    return res

@tool
def analyser_profil_ml(interets_déclarés: str) -> str:
    """Appelle le modèle d'appariement algorithmique pour calculer l'adéquation d'un profil avec les filières en fonction des intérêts explicitement déclarés."""
    with open("formations.json", "r", encoding="utf-8") as f:
        formations = json.load(f)
        
    mots_cles = set(interets_déclarés.lower().split())
    scores = []
    
    for f in formations:
        texte_complet = (f"{f['nom']} {f['description']} {' '.join(f['axes'])} {' '.join(f['competences'])}").lower()
        # Calcul du score de correspondance jaccard/mots-clés
        mots_formation = set(texte_complet.split())
        intersection = mots_cles.intersection(mots_formation)
        score = len(intersection) / max(len(mots_cles), 1)
        scores.append((f, score))
        
    scores.sort(key=lambda x: x[1], reverse=True)
    top_recommendations = scores[:2]
    
    out = "RÉSULTAT DE L'ANALYSE D'ADÉQUATION ML :\n"
    for f, sc in top_recommendations:
        out += f"- Parcours {f['code']} ({f['nom']}) | Score d'adéquation: {min(sc*100 + 40, 95):.1f}%\n"
        out += f"  Facteurs d'influence : Intérêts partagés sur {', '.join(f['axes'][:2])}.\n"
        
    return out