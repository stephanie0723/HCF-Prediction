import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. 读取数据
data = pd.read_excel(r'E:\XJTLU-post\SAT405\长三角\Data\dataset\SN_blank.xlsx', header=0)
X = data.iloc[:, 0:5]
y_f = data["y1-fatigue limit"]
y_s = data["y3-SRI(Stress Range Intercept, MPa)"]

# 2. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y_f, test_size=0.2, random_state=1)
Xs_train, Xs_test, ys_train, ys_test = train_test_split(X, y_s, test_size=0.2, random_state=1)

# 👉 将训练集和测试集合并导出
train_set = pd.concat([X_train, y_train, ys_train], axis=1)
test_set = pd.concat([X_test, y_test, ys_test], axis=1)

train_set.to_excel(r'C:\Users\Administrator\Desktop\train_set.xlsx', index=False)
test_set.to_excel(r'C:\Users\Administrator\Desktop\test_set.xlsx', index=False)

# 3. 初始化并训练模型
model = RandomForestRegressor(n_estimators=200, random_state=1)
model.fit(X_train, y_train)

# 4. 预测
y_pred = model.predict(X_test)

# 5. 模型评估
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"决定系数 R²: {r2:.4f}")
