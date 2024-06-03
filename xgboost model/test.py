import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

model = joblib.load('calorie_model.pkl')  

# 預測數據
data = pd.DataFrame({
    'height': [170],
    'weight': [70],
    'body_fat_percentage': [15],
    'age': [25]
})


prediction = model.predict(data)
print("預測的卡路里摄取量：", prediction)
