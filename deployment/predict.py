import pickle
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd


class Request(BaseModel):
  lead_source: Optional[str] = None
  industry: Optional[str] = None
  employment_status: Optional[str] = None
  location: Optional[str] = None
  number_of_courses_viewed: Optional[int] = None
  annual_income: Optional[float] = None
  interaction_count: Optional[int] = None
  lead_score: Optional[float] = None

app = FastAPI()

def sha256sum(filename):
  with open(filename, 'rb', buffering=0) as file:
    return hashlib.file_digest(file, 'sha256').hexdigest()


def load(filename="pipeline.bin"):
  with open(filename, 'rb') as file:
    model = pickle.load(file)
  return model

@app.get("/")
async def health():
  filename = "pipeline.bin"
  return { filename: sha256sum(filename) }

@app.post("/predict")
async def predict(req: Request):
  model = load("pipeline.bin")
  data = pd.DataFrame([req.model_dump()])
  prediction = model.predict_proba(data)[:, 1]
  return { "probability": float(prediction[0]) }

