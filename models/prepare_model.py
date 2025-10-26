from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def main() -> None:
    iris = load_iris()
    X_train, _, y_train, _ = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    Path("models").mkdir(parents=True, exist_ok=True)
    joblib.dump(model, "models/model.joblib")
    print("Saved models/model.joblib")


if __name__ == "__main__":
    main()
