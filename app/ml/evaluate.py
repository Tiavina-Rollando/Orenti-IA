import json
import os

import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from sklearn.model_selection import train_test_split

from ml.preprocessing import prepare_dataset
from ml.train import build_models


DATASET_PATH = "data/orientation_dataset.csv"
RESULT_PATH = "evaluation/results.json"


def top_k_accuracy(
    probabilities,
    classes,
    y_true,
    k=3
):

    correct = 0

    for probs, true_label in zip(
        probabilities,
        y_true
    ):

        indices = np.argsort(
            probs
        )[::-1][:k]

        predicted_classes = [
            classes[i]
            for i in indices
        ]

        if true_label in predicted_classes:
            correct += 1

    return correct / len(y_true)


def mean_reciprocal_rank(
    probabilities,
    classes,
    y_true
):

    reciprocal_ranks = []

    for probs, true_label in zip(
        probabilities,
        y_true
    ):

        indices = np.argsort(
            probs
        )[::-1]

        ranked_classes = [
            classes[i]
            for i in indices
        ]

        if true_label in ranked_classes:

            rank = (
                ranked_classes.index(
                    true_label
                ) + 1
            )

            reciprocal_ranks.append(
                1 / rank
            )

        else:

            reciprocal_ranks.append(
                0
            )

    return float(
        np.mean(
            reciprocal_ranks
        )
    )


def evaluate_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )

    classes = model.classes_

    results = {

        "accuracy": float(
            accuracy_score(
                y_test,
                predictions
            )
        ),

        "precision_macro": float(
            precision_score(
                y_test,
                predictions,
                average="macro",
                zero_division=0
            )
        ),

        "recall_macro": float(
            recall_score(
                y_test,
                predictions,
                average="macro",
                zero_division=0
            )
        ),

        "f1_macro": float(
            f1_score(
                y_test,
                predictions,
                average="macro",
                zero_division=0
            )
        ),

        "top_1_accuracy": top_k_accuracy(
            probabilities,
            classes,
            y_test,
            k=1
        ),

        "top_3_accuracy": top_k_accuracy(
            probabilities,
            classes,
            y_test,
            k=3
        ),

        "mrr": mean_reciprocal_rank(
            probabilities,
            classes,
            y_test
        ),

        "confusion_matrix": (
            confusion_matrix(
                y_test,
                predictions,
                labels=classes
            ).tolist()
        ),

        "classification_report": (
            classification_report(
                y_test,
                predictions,
                zero_division=0,
                output_dict=True
            )
        )
    }

    return results


def evaluate():

    X, y = prepare_dataset(
        DATASET_PATH
    )

    try:

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42,
                stratify=y
            )
        )

    except ValueError:

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42
            )
        )

    models = build_models()

    results = {}

    for name, model in models.items():

        print(
            f"\nEvaluation : {name}"
        )

        model.fit(
            X_train,
            y_train
        )

        results[name] = evaluate_model(
            model,
            X_test,
            y_test
        )

        print(
            f"Accuracy : "
            f"{results[name]['accuracy']:.4f}"
        )

        print(
            f"F1 macro : "
            f"{results[name]['f1_macro']:.4f}"
        )

        print(
            f"Top-3 : "
            f"{results[name]['top_3_accuracy']:.4f}"
        )

        print(
            f"MRR : "
            f"{results[name]['mrr']:.4f}"
        )

    os.makedirs(
        "evaluation",
        exist_ok=True
    )

    with open(
        RESULT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nRésultats enregistrés : "
        f"{RESULT_PATH}"
    )


if __name__ == "__main__":
    evaluate()