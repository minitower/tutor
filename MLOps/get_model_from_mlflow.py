import mlflow.sklearn
import pandas as pd


df = pd.read_csv("./data/train.csv")

X = df[['Pclass', 'Sex', 'Fare', 'Embarked']]


model = mlflow.sklearn.load_model("models:/titanic_model/1")

preds = model.predict(X)

print(preds)