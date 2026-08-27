import pandas as pd

from data.models import UserProfile
from ml.model_loader import get_models
from ml.preprocessing import profile_to_dataframe


DEFAULT_MODEL = "logistic_regression"


def predict_profile(
    profile: UserProfile,
    model_name: str = DEFAULT_MODEL
):
    """
    Retourne les probabilités prédites pour chaque parcours.
    """

    models = get_models()

    if model_name not in models:
        raise ValueError(
            f"Modèle inconnu : {model_name}. "
            f"Modèles disponibles : "
            f"{list(models.keys())}"
        )

    model = models[model_name]

    X = profile_to_dataframe(
        profile
    )

    probabilities = model.predict_proba(X)[0]

    classes = model.classes_

    predictions = []

    for parcours, probability in zip(
        classes,
        probabilities
    ):
        predictions.append(
            {
                "parcours": str(parcours),
                "score": float(probability)
            }
        )

    predictions.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return predictions