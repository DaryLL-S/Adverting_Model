import numpy as np
import pandas as pd
import xgboost as xgb
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import plot_importance


# 导入数据集
df = pd.read_csv("../W2V_model/result/final_result.csv")
df = df.fillna(value=-1)
data = df.iloc[:, 3:16]

print(data)

model = xgb.Booster(model_file='XGboost.model')
y_pred = model.predict(xgb.DMatrix(data))
yprob = np.argmax(y_pred, axis=1)  # return the index of the biggest pro
predictions = [round(value) for value in yprob]

df2 = pd.read_csv("../W2V_model/result/final_result.csv")
df2['label'] = predictions
df2.to_csv("data/result_data.csv", index=False)
df2.fillna(value=-1)
data = df.iloc[:, 3:16]

# 增量训练
params_02 = {'process_type': 'update',
             'updater': 'refresh',
             'refresh_leaf': True}

new_model = xgb.train(params_02, xgb.DMatrix(data), xgb_model=model)
new_model.save_model('XGboost.model')