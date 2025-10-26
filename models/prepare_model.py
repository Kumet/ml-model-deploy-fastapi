from __future__ import annotations

import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def main() -> None:
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "file:mlruns")
    experiment_name = os.environ.get("MLFLOW_EXPERIMENT_NAME", "iris-classifier")
    run_name = os.environ.get("MLFLOW_RUN_NAME", "logreg-iris")

    if tracking_uri.startswith("file:"):
        Path(tracking_uri.replace("file:", "", 1)).mkdir(parents=True, exist_ok=True)

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    model = LogisticRegression(max_iter=1000)
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("max_iter", model.max_iter)

        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))
        mlflow.log_metric("accuracy", float(accuracy))

        mlflow.sklearn.log_model(model, artifact_path="model")

        Path("models").mkdir(parents=True, exist_ok=True)
        joblib.dump(model, "models/model.joblib")
        mlflow.log_artifact("models/model.joblib")
        print("Saved models/model.joblib and logged to MLflow")


if __name__ == "__main__":
    main()
