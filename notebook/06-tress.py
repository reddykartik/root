import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import root_mean_squared_error
import xgboost as xgb

## {{{ loading dataset
filename = os.path.join(
    os.path.abspath(".."), "data", 
    "car_fuel_efficiency_2026.csv")
df = pd.read_csv(filename)

## missing values and dtypes
df.info()
null = df.columns[df.isnull().sum() > 0]
df[null] = df[null].fillna(0.0)
df.info()
## splitting 
df_full_train, df_test = train_test_split(
    df, test_size=0.2, random_state=1)
df_train, df_val = train_test_split(
    df_full_train, test_size=0.25, random_state=1)
df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)
df_full_train = df_full_train.reset_index(drop=True)
df_train.shape, df_val.shape, df_test.shape

## transforming/encoding
dv = DictVectorizer(sparse=True)
y_train = df_train.fuel_efficiency_mpg.values
X_train = df_train.drop(
    columns=["fuel_efficiency_mpg"]
    ).to_dict(orient="records")
y_val = df_val.fuel_efficiency_mpg.values
X_val = df_val.drop(
    columns=["fuel_efficiency_mpg"]
    ).to_dict(orient="records")
y_test = df_test.fuel_efficiency_mpg.values
X_test = df_test.drop(
    columns=["fuel_efficiency_mpg"]
    ).to_dict(orient="records")

X_train = dv.fit_transform(X_train)
X_val = dv.transform(X_val)

## }}}

## {{{ Decision Tree Regressor
dree = DecisionTreeRegressor(max_depth=1)
dree.fit(X_train, y_train)
# r2_score: 0.18467954480535198
dree.score(X_val, y_val)

## tree internals
print(export_text(dree, feature_names=list(dv.get_feature_names_out())))
## model_year
print("-----------------------------------------------")
## }}}

## {{{ Random Forest Regressor
forest = RandomForestRegressor(
    n_estimators=10,
    random_state=1,
    n_jobs=-1)
forest.fit(X_train, y_train)
# r2_score: 0.6164000923674039
# forest.score(X_val, y_val)
y_pred = forest.predict(X_val)
rmse = root_mean_squared_error(y_val, y_pred)
print(f"rmse: {rmse}") # 1.8332197358745623
print("-----------------------------------------------")
## }}}

## {{{ Random Forest Regressor -- n_estimators 
for i in [10, 50, 100, 150]:
  forest = RandomForestRegressor(
      n_estimators=i,
      random_state=1,
      n_jobs=-1)
  forest.fit(X_train, y_train)  
  y_pred = forest.predict(X_val)
  rmse = root_mean_squared_error(y_val, y_pred)
  print(f"n_estimator: {i}\nrmse: {round(rmse, 3)}")
  # n_estimators: 150, rmse: 1.769
print("-----------------------------------------------")
## }}}

## {{{ Random Forest Regressor -- max_depth && n_estimators
for depth in [10, 15, 20, 25]:
  scores = []
  for est in [10, 50, 100, 150]:
    forest = RandomForestRegressor(
        n_estimators=est,
        max_depth=depth,
        random_state=1,
        n_jobs=-1)
    forest.fit(X_train, y_train)
    y_pred = forest.predict(X_val)
    rmse = root_mean_squared_error(y_val, y_pred)
    scores.append(rmse)
  score = np.array(scores).mean()
  print(f"max_depth: {depth}")
  print(f"rmse: {score}")
  print(f"----------------------------------------")
# max_depth: 10, rmse: 1.7543924943801008
## }}}

## {{{ Random Forest Regressor --- feature_importances_
forest = RandomForestRegressor(
    n_estimators=10,
    max_depth=20,
    random_state=1,
    n_jobs=-1)
forest.fit(X_train, y_train)
features = dv.get_feature_names_out()
importances = forest.feature_importances_
for feature in [
    "vehicle_weight",
    "horsepower", 
    "acceleration", 
    "engine_displacement"]:
  print(f"{feature}: {importances[np.where(features == feature)[0]]}")
# vehicle_weight: 0.20331344
print("-----------------------------------------------")
## }}}

## {{{ Xgboost
features = list(dv.get_feature_names_out())
dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=features)
dval = xgb.DMatrix(X_val, label=y_val, feature_names=features)
for eta in [0.3, 0.1]:
  xgb_params = {
    "eta": eta,
    "max_depth": 6,
    "min_child_weight": 1,
    "objective": "reg:squarederror",
    "nthread": 8,
    "seed": 1,
    "verbosity": 1,
  }
  model = xgb.train(xgb_params, dtrain, num_boost_round=10)
  y_pred = model.predict(dval)
  rmse = root_mean_squared_error(y_val, y_pred)
  print(f"eta: {eta}, rmse: {rmse}")
# eta: 0.3, rmse: 1.7328164504598558
print("-----------------------------------------------")
## }}}
