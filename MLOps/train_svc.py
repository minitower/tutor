import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin

mlflow.set_experiment("titanic_dataset")

# -------------------------
# Кастомный трансформер
# -------------------------
class MyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.log10(X)


# -------------------------
# Загрузка данных
# -------------------------
df = pd.read_csv("./data/train.csv")

X = df[['Pclass', 'Sex', 'Fare', 'Embarked']]
y = df['Survived']


# -------------------------
# Препроцессинг
# -------------------------
numeric_features = ['Pclass', 'Fare']
categorical_features = ['Sex', 'Embarked']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='Missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features),
])


# -------------------------
# Pipeline модели
# -------------------------
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', SVC())
])


# -------------------------
# MLflow запуск
# -------------------------
with mlflow.start_run():

    # логируем параметры
    mlflow.log_param("model_type", "SVC")

    # сплит
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # обучение
    pipeline.fit(X_train, y_train)

    # предсказания
    y_pred = pipeline.predict(X_test)

    # метрики
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    mlflow.log_metric("accuracy", acc)

    # можно логировать подробнее
    mlflow.log_metric("precision", report["weighted avg"]["precision"])
    mlflow.log_metric("recall", report["weighted avg"]["recall"])
    mlflow.log_metric("f1_score", report["weighted avg"]["f1-score"])

    # логируем модель
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        name="model_svc",
        registered_model_name="titanic_model"
    )

    print("Accuracy:", acc)