# # app/ml/recommender.py
# from typing import List

# from data.loader import FORMATIONS_FILE
# from data.models import (
#     Recommendation,
#     RecommendationResult,
#     UserProfile,
# )
# from ml.predictor import predict_profile

# from typing import List, Dict, Any
# from data.models import UserProfile, Recommendation, RecommendationResult


# def generate_justification(profile: UserProfile, parcours_name: str, top_n_reasons: int = 2) -> str:
#     """
#     Génère une explication lisible basée sur la correspondance entre 
#     les données du profil et les exigences du parcours.
#     """
#     reasons = []

#     # 1. Analyse des notes scolaires fortes (ex: note >= 14)
#     good_grades = [
#         matiere.capitalize() for matiere, note in profile.resultats_scolaires.items() 
#         if note >= 14
#     ]
#     if good_grades:
#         reasons.append(f"Excellents résultats en {', '.join(good_grades[:2])}")

#     # 2. Analyse des matières préférées
#     if profile.matieres_preferees:
#         reasons.append(f"Intérêt marqué pour {', '.join(profile.matieres_preferees[:2])}")

#     # 3. Analyse des compétences déclarées
#     if profile.competences:
#         reasons.append(f"Compétences alignées ({', '.join(profile.competences[:2])})")

#     # 4. Analyse des préférences professionnelles ou centres d'intérêt
#     if profile.preferences_professionnelles:
#         reasons.append(f"Projet professionnel axé sur '{profile.preferences_professionnelles[0]}'")

#     # Assemblage de la justification
#     if not reasons:
#         return f"Correspondance globale avec le profil académique pour {parcours_name}."

#     return " • ".join(reasons[:top_n_reasons])


# # ---------------------------------------------------------
# # Chargement du fichier JSON au démarrage de l'application
# # ---------------------------------------------------------
# import json
# from pathlib import Path
# from typing import Any, Dict, List

# # 1. Définition dynamique du chemin
# # Si ce fichier se trouve dans "D:\Projet\Orenti'IA\app\ml\recommendation.py" :
# # .parent -> app/ml
# # .parent.parent -> app
# # .parent.parent.parent -> Orenti'IA (Racine du projet)
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# JSON_PATH = BASE_DIR / "data" / "formations.json"

# # Alternative : Si vous préférez fixer le chemin absolu directement
# # JSON_PATH = Path(r"D:\Projet\Orenti'IA\data\formations.json")


# def load_formations_db(file_path: Path) -> Dict[str, Dict[str, Any]]:
#     """Charge le fichier JSON et crée un dictionnaire indexé par le code de la formation."""
#     if not file_path.exists():
#         raise FileNotFoundError(
#             f"Le fichier de formations est introuvable à l'emplacement : {file_path}"
#         )

#     with open(file_path, "r", encoding="utf-8") as f:
#         formations_list = json.load(f)

#     return {item["code"]: item for item in formations_list}


# # Base de données chargée au démarrage
# FORMATIONS_DB = load_formations_db(JSON_PATH)

# # ---------------------------------------------------------
# # Fonction de génération de justification
# # ---------------------------------------------------------
# def generate_rich_justification(
#     profile: UserProfile, formation_data: Dict[str, Any]
# ) -> str:
#     """Génère une justification personnalisée basée sur les données de la formation."""
#     reasons = []

#     # 1. Prérequis (Baccalauréat)
#     bac_user = getattr(profile, "serie_bac", None)
#     prerequis_text = formation_data.get("prerequis", "")

#     if bac_user:
#         if "toutes séries" in prerequis_text.lower():
#             reasons.append(f"Bac {bac_user} éligible")
#         elif bac_user.upper() in prerequis_text.upper():
#             reasons.append(f"Bac {bac_user} conforme aux prérequis")

#     # 2. Axes / Centres d'intérêt
#     user_interests = getattr(profile, "centres_interet", []) or getattr(
#         profile, "matieres_preferees", []
#     )
#     matching_axes = []
#     for axe in formation_data.get("axes", []):
#         for interest in user_interests:
#             if interest.lower() in axe.lower() or axe.lower() in interest.lower():
#                 matching_axes.append(axe)
#                 break

#     if matching_axes:
#         reasons.append(
#             f"Axes d'étude alignés avec vos intérêts ({', '.join(matching_axes[:2])})"
#         )

#     # 3. Compétences
#     user_skills = getattr(profile, "competences", [])
#     matching_skills = []
#     for comp in formation_data.get("competences", []):
#         for skill in user_skills:
#             if skill.lower() in comp.lower() or comp.lower() in skill.lower():
#                 matching_skills.append(comp)
#                 break

#     if matching_skills:
#         reasons.append(f"Compétences visées : {', '.join(matching_skills[:2])}")

#     # 4. Métier visé / Débouchés
#     target_job = getattr(profile, "metier_vise", None)
#     if not target_job:
#         prefs = getattr(profile, "preferences_professionnelles", [])
#         if prefs:
#             target_job = prefs[0]

#     if target_job:
#         matching_jobs = [
#             job
#             for job in formation_data.get("debouches", [])
#             if target_job.lower() in job.lower() or job.lower() in target_job.lower()
#         ]
#         if matching_jobs:
#             reasons.append(
#                 f"Prépare directement au métier visé ({matching_jobs[0]})"
#             )

#     if not reasons:
#         domaine = formation_data.get("domaine", "ce domaine")
#         return f"Formation adaptée à votre profil dans le domaine {domaine}."

#     return " • ".join(reasons)


# # ---------------------------------------------------------
# # Fonction de recommandation
# # ---------------------------------------------------------
# def generate_recommendations(
#     profile: UserProfile,
#     top_k: int = 3,
#     model_name: str = "logistic_regression",
# ) -> RecommendationResult:

#     predictions = predict_profile(profile, model_name=model_name)
#     recommendations: List[Recommendation] = []

#     for prediction in predictions[:top_k]:
#         score = prediction["score"]
#         parcours_code = prediction["parcours"]

#         # Récupération des données depuis FORMATIONS_DB
#         formation_info = FORMATIONS_DB.get(parcours_code, {})

#         # Génération de la justification
#         justification = generate_rich_justification(profile, formation_info)

#         recommendations.append(
#             Recommendation(
#                 parcours=parcours_code,
#                 score=round(score, 4),
#                 justification=justification,
#             )
#         )

#     return RecommendationResult(recommendations=recommendations)

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from data.loader import FORMATIONS_FILE
from data.models import (
    Recommendation,
    RecommendationResult,
    UserProfile,
)
from ml.predictor import predict_profile


def get_resource_path(relative_path: str) -> Path:
    """Résout le chemin absolu d'une ressource (Compatible Dev et PyInstaller .exe)."""
    if hasattr(sys, "_MEIPASS"):
        # Mode exécution Pyinstaller
        return Path(sys._MEIPASS) / relative_path
    
    # Mode développement classique : racine du projet
    return Path(__file__).resolve().parent.parent.parent / relative_path


# Résolution dynamique du chemin vers formations.json
JSON_PATH = get_resource_path("data/formations.json")


def load_formations_db(file_path: Path) -> Dict[str, Dict[str, Any]]:
    """Charge le fichier JSON et crée un dictionnaire indexé par le code de la formation."""
    if not file_path.exists():
        # Fallback de sécurité si le fichier n'est pas dans _MEIPASS
        fallback_path = Path.cwd() / "data" / "formations.json"
        if fallback_path.exists():
            file_path = fallback_path
        else:
            raise FileNotFoundError(
                f"Le fichier de formations est introuvable à : {file_path}"
            )

    with open(file_path, "r", encoding="utf-8") as f:
        formations_list = json.load(f)

    return {item["code"]: item for item in formations_list}


# Chargement sécurisé de la base de données
try:
    FORMATIONS_DB = load_formations_db(JSON_PATH)
except Exception as e:
    FORMATIONS_DB = {}
    print(f"⚠️ Avertissement lors du chargement du JSON : {e}")


def generate_rich_justification(
    profile: UserProfile, formation_data: Dict[str, Any]
) -> str:
    """Génère une justification personnalisée basée sur les données de la formation."""
    reasons = []

    # 1. Prérequis (Baccalauréat)
    bac_user = getattr(profile, "serie_bac", None)
    prerequis_text = formation_data.get("prerequis", "")

    if bac_user:
        if "toutes séries" in prerequis_text.lower():
            reasons.append(f"Bac {bac_user} éligible")
        elif bac_user.upper() in prerequis_text.upper():
            reasons.append(f"Bac {bac_user} conforme aux prérequis")

    # 2. Axes / Centres d'intérêt
    user_interests = getattr(profile, "centres_interet", []) or getattr(
        profile, "matieres_preferees", []
    )
    matching_axes = []
    for axe in formation_data.get("axes", []):
        for interest in user_interests:
            if interest.lower() in axe.lower() or axe.lower() in interest.lower():
                matching_axes.append(axe)
                break

    if matching_axes:
        reasons.append(
            f"Axes d'étude alignés avec vos intérêts ({', '.join(matching_axes[:2])})"
        )

    # 3. Compétences
    user_skills = getattr(profile, "competences", [])
    matching_skills = []
    for comp in formation_data.get("competences", []):
        for skill in user_skills:
            if skill.lower() in comp.lower() or comp.lower() in skill.lower():
                matching_skills.append(comp)
                break

    if matching_skills:
        reasons.append(f"Compétences visées : {', '.join(matching_skills[:2])}")

    # 4. Métier visé / Débouchés
    target_job = getattr(profile, "metier_vise", None)
    if not target_job:
        prefs = getattr(profile, "preferences_professionnelles", [])
        if prefs:
            target_job = prefs[0]

    if target_job:
        matching_jobs = [
            job
            for job in formation_data.get("debouches", [])
            if target_job.lower() in job.lower() or job.lower() in target_job.lower()
        ]
        if matching_jobs:
            reasons.append(
                f"Prépare directement au métier visé ({matching_jobs[0]})"
            )

    if not reasons:
        domaine = formation_data.get("domaine", "ce domaine")
        return f"Formation adaptée à votre profil dans le domaine {domaine}."

    return " • ".join(reasons)


def generate_recommendations(
    profile: UserProfile,
    top_k: int = 3,
    model_name: str = "logistic_regression",
) -> RecommendationResult:

    # S'assurer que la base est chargée
    global FORMATIONS_DB
    if not FORMATIONS_DB:
        FORMATIONS_DB = load_formations_db(JSON_PATH)

    predictions = predict_profile(profile, model_name=model_name)
    recommendations: List[Recommendation] = []

    for prediction in predictions[:top_k]:
        score = prediction["score"]
        parcours_code = prediction["parcours"]

        formation_info = FORMATIONS_DB.get(parcours_code, {})
        justification = generate_rich_justification(profile, formation_info)

        recommendations.append(
            Recommendation(
                parcours=parcours_code,
                score=round(score, 4),
                justification=justification,
            )
        )

    return RecommendationResult(recommendations=recommendations)