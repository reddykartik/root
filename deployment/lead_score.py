import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def load(filepath):
  # loading dataset
  df = pd.read_csv(filepath)
  X = df.drop(columns=["converted"])
  y = df.converted.values
  return X, y

def create_pipeline(nums, cat):
  # --- numerical pipeline ---
  numerical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
  ])

  # --- categorical pipeline ---
  categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="NA")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
  ])

  # --- Combine ---
  preprocessor = ColumnTransformer(transformers=[
    ("nums", numerical_transformer, nums),
    ("cat", categorical_transformer, cat),
  ])

  # --- model ---
  model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(solver="liblinear", C=1.0)),
  ])

  return model

def split(X, y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11, stratify=y)
  return X_train, X_test, y_train, y_test

def score(y_true, y_pred, threshold=0.5):
  roc_auc = roc_auc_score(y_true, y_pred >= threshold)
  report = classification_report(y_true, y_pred >= threshold)
  matrix = confusion_matrix(y_true, y_pred >= threshold)
  print(f"roc_auc: {roc_auc}")
  print(f"classification_report: {report}")
  print(f"confusion_matrix: {matrix}")

def write(model, filename="pipeline.bin"):
  with open(filename, "wb") as file:
    pickle.dump(model, file)
  print(f"model is saved in {filename}")

if __name__ == '__main__':
  filepath = os.path.join(os.path.abspath(".."), "data", "course_lead_scoring_2026.csv")
  X, y = load(filepath)
  nums = X.select_dtypes(include=[np.number]).columns
  cat = X.select_dtypes(include=["object", "str"]).columns
  X_train, X_test, y_train, y_test = split(X, y)
  model = create_pipeline(nums, cat)
  model.fit(X_train, y_train)
  y_pred = model.predict_proba(X_test)[:, 1]
  score(y_test, y_pred)
  write(model)
