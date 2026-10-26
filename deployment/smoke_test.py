import pickle
import pandas as pd

def load(filename="pipeline.bin"):
  with open(filename, 'rb') as file:
    model = pickle.load(file)
  return model

if __name__ == '__main__':
  data = pd.DataFrame([{
    "lead_source": "paid_ads",
    "industry": "technology",
    "employment_status": "employed",
    "location": "north_america",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0,
    "interaction_count": 4,
    "lead_score": 0.41
  }])

  model = load()
  y_pred = model.predict_proba(data)[:, 1]
  print(f"y_pred: {y_pred.round(3)}")

