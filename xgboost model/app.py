import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import joblib

# 讀取 JSON 檔案
def load_data(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

# 預處理數據
def preprocess_data(df):
    df = df.fillna(df.mean())
    return df

# 訓練模型
def train_model(X, y, model_type='random_forest'):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'decision_tree':
        model = DecisionTreeRegressor(random_state=42)
    elif model_type == 'xgboost':
        model = XGBRegressor(objective='reg:squarederror', random_state=42)
    else:
        raise ValueError("Unsupported model type")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"{model_type} MSE: {mse}")
    return model

# 儲存模型
def save_model(model, file_path):
    joblib.dump(model, file_path)


def main(input_json_path, model_output_path, model_type='random_forest'):
    df = load_data(input_json_path)
    df = preprocess_data(df)
    X = df.drop(columns=['calories'])  
    y = df['calories']
    model = train_model(X, y, model_type=model_type)
    save_model(model, model_output_path)

input_json_path = 'data.json'  
model_output_path = 'calorie_model.pkl' 
model_type = 'xgboost'  

main(input_json_path, model_output_path, model_type)
