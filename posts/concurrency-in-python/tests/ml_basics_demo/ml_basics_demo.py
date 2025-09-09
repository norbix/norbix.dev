# ml_basics_demo.py
"""
Mini demo: Data/ML basics (metrics, preprocessing)
Run:
  python ml_basics_demo.py preprocess-text
  python ml_basics_demo.py preprocess-numeric
  python ml_basics_demo.py metrics-classification
  python ml_basics_demo.py metrics-regression
"""

from __future__ import annotations
import argparse
import math
import re
from collections import Counter, defaultdict

# --------------------------
# Text preprocessing (simple)
# --------------------------

_PUNCT_RE = re.compile(r"[^\w\s]")
_STOPWORDS = {"a", "an", "the", "and", "or", "is", "are", "to", "of", "in"}

def tokenize(text: str) -> list[str]:
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    tokens = [t for t in text.split() if t and t not in _STOPWORDS]
    return tokens

def build_vocab(texts: list[str], max_size: int = 10) -> list[str]:
    counter = Counter()
    for t in texts:
        counter.update(tokenize(t))
    vocab = [w for w, _ in counter.most_common(max_size)]
    return vocab

def vectorize(text: str, vocab: list[str]) -> list[int]:
    tokens = tokenize(text)
    counts = Counter(tokens)
    return [counts.get(w, 0) for w in vocab]

# --------------------------
# Numeric preprocessing
# --------------------------

def minmax_scale(xs: list[float]) -> list[float]:
    lo, hi = min(xs), max(xs)
    if hi == lo:
        return [0.0 for _ in xs]
    return [(x - lo) / (hi - lo) for x in xs]

def zscore(xs: list[float]) -> list[float]:
    n = len(xs)
    mu = sum(xs) / n
    var = sum((x - mu) ** 2 for x in xs) / n
    std = math.sqrt(var)
    if std == 0:
        return [0.0 for _ in xs]
    return [(x - mu) / std for x in xs]

def one_hot(categories: list[str]) -> tuple[list[str], list[list[int]]]:
    uniq = sorted(set(categories))
    index = {c: i for i, c in enumerate(uniq)}
    vecs = []
    for c in categories:
        v = [0] * len(uniq)
        v[index[c]] = 1
        vecs.append(v)
    return uniq, vecs

# --------------------------
# Classification metrics (binary)
# --------------------------

def classification_report(y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    # assume labels {0,1}
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    acc = (tp + tn) / max(1, len(y_true))
    prec = tp / max(1, (tp + fp))
    rec = tp / max(1, (tp + fn))
    if prec + rec == 0:
        f1 = 0.0
    else:
        f1 = 2 * prec * rec / (prec + rec)
    return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}

# --------------------------
# Regression metrics
# --------------------------

def regression_report(y_true: list[float], y_pred: list[float]) -> dict[str, float]:
    n = len(y_true)
    mae = sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / n
    mse = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / n
    rmse = math.sqrt(mse)
    mu = sum(y_true) / n
    ss_tot = sum((yt - mu) ** 2 for yt in y_true)
    ss_res = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}

# --------------------------
# Demo runners
# --------------------------

def run_preprocess_text():
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Quick movement and fast foxes are amazing!",
        "Dogs are loyal and quick to learn.",
    ]
    vocab = build_vocab(texts, max_size=8)
    X = [vectorize(t, vocab) for t in texts]
    print("[preprocess-text] vocab:", vocab)
    for i, row in enumerate(X):
        print(f"  doc{i}: {row}")

def run_preprocess_numeric():
    heights = [170.0, 180.0, 160.0, 175.0, 165.0]
    cities = ["KRK", "WAW", "WAW", "GDA", "KRK"]

    print("[preprocess-numeric] raw heights:", heights)
    print("  minmax:", [round(x, 3) for x in minmax_scale(heights)])
    print("  zscore:", [round(x, 3) for x in zscore(heights)])

    cats, oh = one_hot(cities)
    print("  categories:", cats)
    for i, row in enumerate(oh):
        print(f"  onehot{i} ({cities[i]}): {row}")

def run_metrics_classification():
    # toy ground truth and predictions
    y_true = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
    y_pred = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0]
    rep = classification_report(y_true, y_pred)
    print("[metrics-classification]")
    for k, v in rep.items():
        print(f"  {k}: {v:.3f}")

def run_metrics_regression():
    y_true = [3.2, 4.0, 5.5, 6.1, 7.0]
    y_pred = [3.0, 4.3, 5.0, 6.2, 6.8]
    rep = regression_report(y_true, y_pred)
    print("[metrics-regression]")
    for k, v in rep.items():
        print(f"  {k}: {v:.3f}")

# --------------------------
# CLI
# --------------------------

def main():
    p = argparse.ArgumentParser(description="Simplest ML basics demo")
    p.add_argument("mode", choices=[
        "preprocess-text",
        "preprocess-numeric",
        "metrics-classification",
        "metrics-regression",
    ])
    args = p.parse_args()

    if args.mode == "preprocess-text":
        run_preprocess_text()
    elif args.mode == "preprocess-numeric":
        run_preprocess_numeric()
    elif args.mode == "metrics-classification":
        run_metrics_classification()
    elif args.mode == "metrics-regression":
        run_metrics_regression()

if __name__ == "__main__":
    main()
