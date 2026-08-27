import os
import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from app.ml.preprocessing import SUBJECT_COLUMNS, prepare_dataset

DATASET_PATH = "data/orientation_dataset.csv"
MODEL_PATH = "models/orientation_model.pkl"


def build_preprocessor():
    text_features = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True, ngram_range=(1, 2), min_df=1
                ),
            )
        ]
    )

    numeric_features = Pipeline(steps=[("scaler", StandardScaler())])

    # Inscription de TOUTES les colonnes numériques du dataset
    numeric_columns = ["note_moyenne", "note_max", "note_min"] + SUBJECT_COLUMNS

    preprocessor = ColumnTransformer(
        transformers=[
            ("text", text_features, "profile_text"),
            ("numeric", numeric_features, numeric_columns),
        ]
    )

    return preprocessor


def build_models():
    preprocessor = build_preprocessor()

    logistic_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(max_iter=2000, random_state=42),
            ),
        ]
    )

    svm_model = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", SVC(probability=True, kernel="linear", random_state=42)),
        ]
    )

    baseline_model = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "classifier",
                DummyClassifier(strategy="most_frequent", random_state=42),
            ),
        ]
    )

    return {
        "baseline": baseline_model,
        "logistic_regression": logistic_model,
        "svm": svm_model,
    }


def train():
    print("=" * 60)
    print("ENTRAINEMENT DU MODELE ORIENT'IA")
    print("=" * 60)

    X, y = prepare_dataset(DATASET_PATH)

    print(f"Nombre de profils : {len(X)}")
    print(f"Nombre de parcours : {y.nunique()}")

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )
    except ValueError:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42
        )

    models = build_models()
    trained_models = {}

    for name, model in models.items():
        print(f"\nEntraînement : {name}")
        model.fit(X_train, y_train)
        trained_models[name] = model

    os.makedirs("models", exist_ok=True)

    artifact = {
        "models": trained_models,
        "classes": sorted(y.unique().tolist()),
        "feature_columns": X.columns.tolist(),
    }

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(artifact, file)

    print(f"\nModèles sauvegardés dans : {MODEL_PATH}")
    print("\nEntraînement terminé.")


if __name__ == "__main__":
    train()