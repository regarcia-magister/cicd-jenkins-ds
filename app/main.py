from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


@dataclass
class TrainResult:
    accuracy: float
    n_train: int
    n_test: int


def train(random_state: int = 42) -> TrainResult:
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=random_state, stratify=data.target
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = float(accuracy_score(y_test, preds))

    return TrainResult(accuracy=acc, n_train=len(X_train), n_test=len(X_test))


def save_metrics(result: TrainResult, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"accuracy": result.accuracy, "n_train": result.n_train, "n_test": result.n_test}
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Mini DS pipeline: train + metrics")
    p.add_argument("--out", default="artifacts/metrics.json", help="Output metrics path")
    p.add_argument("--random-state", type=int, default=42)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = train(random_state=args.random_state)
    save_metrics(result, Path(args.out))
    print(f"accuracy={result.accuracy:.4f} n_train={result.n_train} n_test={result.n_test}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
