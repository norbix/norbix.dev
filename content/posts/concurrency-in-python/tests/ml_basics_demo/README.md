# What this shows (at a glance):

- Text: lowercase → strip punctuation → remove stopwords → tiny bag-of-words vectors.

- Numeric: min–max scaling, z-score normalization, one-hot encoding.

- Classification metrics: accuracy, precision, recall, F1 (binary).

- Regression metrics: MAE, MSE, RMSE, R².

Want a follow-up version using NumPy/Pandas + scikit-learn with the equivalent transformers/metrics so readers can compare “from scratch” vs “library” style?

```shell
python ml_basics_demo.py preprocess-text
#python ml_basics_demo.py preprocess-numeric
#python ml_basics_demo.py metrics-classification
#python ml_basics_demo.py metrics-regression
```
