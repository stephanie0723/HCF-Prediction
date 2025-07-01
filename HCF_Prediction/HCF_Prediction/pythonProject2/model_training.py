import pickle
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def train_and_save_models():
    # 读取数据
    data = pd.read_excel(r'C:\Users\Administrator\HCF_Prediction\pythonProject2\dataset\train_set.xlsx', header=0)

    # 定义输入特征和两个目标变量
    X = data.iloc[:, 0:5]
    y_f = data["y1-fatigue limit"]
    y_s = data["y3-SRI(Stress Range Intercept, MPa)"]

    # 训练 Fatigue Limit 模型
    rf_fatigue = RandomForestRegressor(n_estimators=200, random_state=1)
    rf_fatigue.fit(X, y_f)

    # 保存 Fatigue Limit 模型
    with open('rf_fatigue_model.pkl', 'wb') as f:
        pickle.dump(rf_fatigue, f)

    # 训练 SRI 模型
    rf_sri = RandomForestRegressor(n_estimators=200, random_state=1)
    rf_sri.fit(X, y_s)

    # 保存 SRI 模型
    with open('rf_sri_model.pkl', 'wb') as f:
        pickle.dump(rf_sri, f)

if __name__ == '__main__':
    train_and_save_models()
