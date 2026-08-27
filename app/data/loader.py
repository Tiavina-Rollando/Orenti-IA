import json
import sys
from pathlib import Path

from data.models import UserProfile


# =========================================================
# CHEMIN DE BASE DE L'APPLICATION
# =========================================================

def get_base_path():

    # Application exécutée avec PyInstaller
    if getattr(sys, "frozen", False):

        return Path(sys._MEIPASS)

    # Application exécutée normalement avec Python
    return Path(__file__).resolve().parents[2]


BASE_PATH = get_base_path()


# =========================================================
# DOSSIER DATA
# =========================================================

DATA_PATH = BASE_PATH / "data"


# =========================================================
# FICHIERS DE DONNÉES
# =========================================================

PROFILE_FILE = DATA_PATH / "profile.json"

FORMATIONS_FILE = DATA_PATH / "formations.json"


# =========================================================
# CHARGER LE PROFIL
# =========================================================

def load_profile() -> UserProfile:

    """
    Charge le profil utilisateur depuis profile.json.

    Si le fichier n'existe pas ou si son contenu
    est invalide, un profil vide est retourné.
    """

    if not PROFILE_FILE.exists():

        return UserProfile()

    try:

        with open(
            PROFILE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return UserProfile(
            **data
        )

    except (
        json.JSONDecodeError,
        TypeError,
        ValueError
    ):

        return UserProfile()


# =========================================================
# SAUVEGARDER LE PROFIL
# =========================================================

def save_profile(
    profile: UserProfile
):

    """
    Sauvegarde le profil utilisateur
    dans data/profile.json.
    """

    DATA_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        PROFILE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profile.model_dump(),
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================================================
# CHARGER LES FORMATIONS
# =========================================================

def load_formations():

    """
    Charge les formations depuis formations.json.

    Retourne une liste vide si le fichier
    n'existe pas ou contient des données invalides.
    """

    if not FORMATIONS_FILE.exists():

        return []

    try:

        with open(
            FORMATIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        # Vérification simple :
        # formations.json doit contenir une liste.

        if not isinstance(
            data,
            list
        ):

            return []

        return data

    except (
        json.JSONDecodeError,
        TypeError
    ):

        return []