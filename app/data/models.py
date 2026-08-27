from pydantic import BaseModel, Field
from typing import List, Optional


class UserProfile(BaseModel):
    """
    Profil d'un étudiant utilisé pour l'orientation.
    Les champs correspondent aux caractéristiques
    utilisées par le modèle de Machine Learning.
    """

    # ---------------------------------------------------------
    # INFORMATIONS ACADÉMIQUES
    # ---------------------------------------------------------

    niveau: str = ""

    matieres_preferees: List[str] = Field(default_factory=list)

    resultats_scolaires: dict[str, float] = Field(
        default_factory=dict
    )

    # Exemple :
    # {
    #     "Mathématiques": 15,
    #     "Français": 12,
    #     "Physique": 14
    # }

    # ---------------------------------------------------------
    # COMPÉTENCES
    # ---------------------------------------------------------

    competences: List[str] = Field(
        default_factory=list
    )

    # Exemple :
    # ["Python", "Programmation", "Communication"]

    # ---------------------------------------------------------
    # CENTRES D'INTÉRÊT
    # ---------------------------------------------------------

    centres_interet: List[str] = Field(
        default_factory=list
    )

    # Exemple :
    # ["Intelligence artificielle", "Informatique", "Business"]

    # ---------------------------------------------------------
    # ACTIVITÉS / PROJETS
    # ---------------------------------------------------------

    activites_projets: List[str] = Field(
        default_factory=list
    )

    # Exemple :
    # [
    #     "Création d'une application Python",
    #     "Projet Arduino",
    #     "Participation à un hackathon"
    # ]

    # ---------------------------------------------------------
    # PRÉFÉRENCES PROFESSIONNELLES
    # ---------------------------------------------------------

    preferences_professionnelles: List[str] = Field(
        default_factory=list
    )

    # Exemple :
    # [
    #     "Développeur logiciel",
    #     "Data Scientist",
    #     "Entrepreneur"
    # ]

    # ---------------------------------------------------------
    # ENVIRONNEMENT DE TRAVAIL
    # ---------------------------------------------------------

    environnement_travail: List[str] = Field(
        default_factory=list
    )

    # Exemple :
    # [
    #     "Travail en équipe",
    #     "Bureau",
    #     "Laboratoire"
    # ]


class Recommendation(BaseModel):

    parcours: str
    score: float
    justification: Optional[str] = None

    # Exemple:
    # Recommendation(
    #     parcours="IGGLIA",
    #     score=0.91,
    #     justification="Forte correspondance avec les compétences en programmation et l'intérêt pour l'IA."
    # )

class RecommendationResult(BaseModel):
    """Conteneur qui regroupe la liste des recommandations retournées."""

    recommendations: List[Recommendation] = Field(default_factory=list)