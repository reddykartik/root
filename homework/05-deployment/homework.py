import pickle

def load():
  # open the saved model file in binary read mode
  with open('pipeline.bin', 'rb') as file:
    # load the model object from the file 
    model = pickle.load(file)
  return model


def main():
  data = {
      "lead_source": "paid_ads",
      "industry": "technology",
      "employment_status": "employed",
      "location": "north_america",
      "number_of_courses_viewed": 2,
      "annual_income": 79276.0,
      "interaction_count": 4,
      "lead_score": 0.41,
      }

  model = load()
  y_pred = model.predict_proba(data)[:, 1]
  print(f"y_pred: {y_pred}")
  print(f"rounded y_pred: {y_pred.round(3)}")

if __name__ == '__main__':
  main()
