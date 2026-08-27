import os
import pickle


MODEL_PATH = "models/orientation_model.pkl"


_model_artifact = None


def load_model():

    global _model_artifact

    if _model_artifact is not None:
        return _model_artifact

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Modèle introuvable : {MODEL_PATH}\n"
            "Lancez d'abord train.py."
        )

    with open(
        MODEL_PATH,
        "rb"
    ) as file:

        _model_artifact = pickle.load(
            file
        )

    return _model_artifact


def get_models():

    artifact = load_model()

    return artifact["models"]


def get_classes():

    artifact = load_model()

    return artifact["classes"]