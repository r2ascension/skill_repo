# Machine Learning Foundations

## Environment

```bash
conda create -n ml_base python=3.10
conda activate ml_base
pip install numpy pandas matplotlib seaborn scikit-learn umap-learn
```

Keep package versions in an environment file when reproducing notebook results.

## Visualization

Matplotlib examples:

```python
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```

Seaborn examples:

```python
import seaborn as sns
sns.scatterplot(data=df, x="x", y="y", hue="group")
sns.boxplot(data=df, x="group", y="value")
sns.histplot(data=df, x="value", hue="group", kde=True)
```

## Basic sklearn Pattern

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

X = df.drop(columns=["label"])
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000))
])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(classification_report(y_test, pred))
```

## Preprocessing

Use `StandardScaler` for models sensitive to feature scale, such as SVM, KNN, logistic regression, PCA, and many clustering methods. Use `MinMaxScaler` when a bounded range is desired.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
X_std = StandardScaler().fit_transform(X)
X_mm = MinMaxScaler().fit_transform(X)
```

## Unsupervised Learning

PCA:

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
coords = pca.fit_transform(X_std)
print(pca.explained_variance_ratio_)
```

K-means:

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, random_state=42, n_init="auto")
labels = km.fit_predict(X_std)
```

Evaluate cluster number with elbow plots, silhouette scores, and domain interpretability.

## Supervised Classification

Typical beginner models:

- Logistic regression.
- Linear discriminant analysis.
- Decision tree.
- Random forest.
- Support vector machine.
- K-nearest neighbors.
- Gradient boosting.

Use stratified splits for class imbalance and report precision, recall, F1, and confusion matrix, not just accuracy.

## Regression

```python
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, r2_score

reg = LinearRegression().fit(X_train, y_train)
pred = reg.predict(X_test)
print(mean_squared_error(y_test, pred), r2_score(y_test, pred))

lasso = Lasso(alpha=0.1).fit(X_train, y_train)
```

Use regularization when features are numerous or correlated.

## Model Evaluation

```python
from sklearn.model_selection import cross_val_score, GridSearchCV

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")

params = {"clf__C": [0.1, 1, 10]}
search = GridSearchCV(model, params, cv=5, scoring="f1_macro")
search.fit(X_train, y_train)
```

Keep preprocessing inside the pipeline to prevent data leakage.

## Dimensionality Reduction And Clustering

Include LDA, t-SNE, and UMAP only when they answer an interpretation or visualization question. For t-SNE and UMAP, set random seeds and avoid overinterpreting distances between far-apart clusters.

## Text Mining

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

vec = TfidfVectorizer(max_features=5000)
X_text = vec.fit_transform(texts)
clf = MultinomialNB().fit(X_text, labels)
```

Use tokenization appropriate to the language and domain.
