from typing import Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# 1. Modèle UserProfile (si besoin dans app.data.models)
# -------------------------------------------------------------------
class UserProfile(BaseModel):
    niveau: Optional[str] = None
    matieres_preferees: Optional[List[str]] = Field(default_factory=list)
    competences: Optional[List[str]] = Field(default_factory=list)
    centres_interet: Optional[List[str]] = Field(default_factory=list)
    activites_projets: Optional[List[str]] = Field(default_factory=list)
    preferences_professionnelles: Optional[List[str]] = Field(
        default_factory=list
    )
    environnement_travail: Optional[List[str]] = Field(default_factory=list)
    resultats_scolaires: Dict[str, float] = Field(
        default_factory=dict
    )  # ex: {"mathematiques": 15.5, "anglais": 14.0}


# -------------------------------------------------------------------
# 2. Colonnes du Dataset
# -------------------------------------------------------------------
TEXT_COLUMNS = [
    "matieres_preferees",
    "competences",
    "centres_interet",
    "activites_projets",
    "preferences_professionnelles",
    "environnement_travail",
]

SUBJECT_COLUMNS = [
    "mathematiques",
    "physique",
    "chimie",
    "informatique",
    "francais",
    "anglais",
    "biologie",
    "economie",
    "gestion",
    "histoire_geographie",
    "droit",
    "technique",
]


def normalize_list(value) -> str:
    """Transforme une liste ou une chaîne séparée par des points-virgules

    en texte nettoyé pour le TF-IDF.
    """
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(str(item).strip() for item in value if item)

    if pd.isna(value):
        return ""

    return str(value).replace(";", " ")


def profile_to_dataframe(profile: UserProfile) -> pd.DataFrame:
    """Transforme un UserProfile (instance Pydantic) en DataFrame d'une seule

    ligne compatible avec les fonctionnalités créées lors de la préparation du
    dataset.
    """
    notes = profile.resultats_scolaires or {}
    notes_values = [v for v in notes.values() if v > 0]

    row = {
        "niveau": profile.niveau or "",
        "matieres_preferees": normalize_list(profile.matieres_preferees),
        "competences": normalize_list(profile.competences),
        "centres_interet": normalize_list(profile.centres_interet),
        "activites_projets": normalize_list(profile.activites_projets),
        "preferences_professionnelles": normalize_list(
            profile.preferences_professionnelles
        ),
        "environnement_travail": normalize_list(profile.environnement_travail),
    }

    # Ajouter les notes individuelles par matière
    for subj in SUBJECT_COLUMNS:
        row[subj] = float(notes.get(subj, 0.0))

    # Calcul des statistiques sur les notes
    row["note_moyenne"] = (
        sum(notes_values) / len(notes_values) if notes_values else 0.0
    )
    row["note_max"] = max(notes_values) if notes_values else 0.0
    row["note_min"] = min(notes_values) if notes_values else 0.0

    # Texte global de synthèse
    row["profile_text"] = (
        f"{row['niveau']} {row['matieres_preferees']} {row['competences']} "
        f"{row['centres_interet']} {row['activites_projets']} "
        f"{row['preferences_professionnelles']} {row['environnement_travail']}"
    )

    return pd.DataFrame([row])


def prepare_dataset(csv_path: str):
    """Charge et prépare le dataset d'entraînement à partir du fichier CSV.

    Retourne :
        X : DataFrame avec le texte assemblé, les notes par matière et les agrégats de notes.
        y : Série avec les parcours cibles.
    """
    df = pd.read_csv(csv_path)

    required_columns = (
        ["niveau", "parcours_recommande"] + TEXT_COLUMNS + SUBJECT_COLUMNS
    )

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            "Colonnes manquantes dans le dataset : " + ", ".join(missing)
        )

    # Nettoyage des cibles manquantes
    df = df.dropna(subset=["parcours_recommande"]).copy()

    # Normalisation des textes
    for column in TEXT_COLUMNS:
        df[column] = df[column].apply(normalize_list)

    # Nettoyage des colonnes de notes
    for subj in SUBJECT_COLUMNS:
        df[subj] = pd.to_numeric(df[subj], errors="coerce").fillna(0.0)

    # Calcul des statistiques de notes par élève (en ignorant les notes à 0 = non suivies)
    df_notes = df[SUBJECT_COLUMNS].replace(0.0, pd.NA)

    df["note_moyenne"] = df_notes.mean(axis=1).fillna(0.0)
    df["note_max"] = df_notes.max(axis=1).fillna(0.0)
    df["note_min"] = df_notes.min(axis=1).fillna(0.0)

    # Construction du texte global pour TF-IDF / Embeddings
    df["profile_text"] = (
        df["niveau"].fillna("")
        + " "
        + df["matieres_preferees"]
        + " "
        + df["competences"]
        + " "
        + df["centres_interet"]
        + " "
        + df["activites_projets"]
        + " "
        + df["preferences_professionnelles"]
        + " "
        + df["environnement_travail"]
    )

    # Définition des features X (Texte + Agrégats + Notes par matière)
    feature_columns = [
        "profile_text",
        "note_moyenne",
        "note_max",
        "note_min",
    ] + SUBJECT_COLUMNS

    X = df[feature_columns]
    y = df["parcours_recommande"]

    return X, y