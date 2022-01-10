import pandas as pd
import xgboost as xgb
from matplotlib import pyplot as plt
from xgboost import plot_importance

# 导入数据集
df = pd.read_csv("./data/raw_data.csv")
df = df.fillna(value=-1)
data = df.iloc[:, 3:16]
target = df.iloc[:, -1:]

print(data)
print(target)

# booster:
params = {'learning_rate': 0.4,
          'max_depth': 20,  # 构建树的深度，越大越容易过拟合
          'num_boost_round': 2000,
          'objective': 'multi:softprob',  # 多分类的问题
          'random_state': 7,
          'silent': 0,
          'num_class': 5,  # 类别数，与 multisoftmax 并用
          'eta': 0.8}

model = xgb.train(params, xgb.DMatrix(data, target))
model.save_model('XGboost.model')

# 显示重要特征
plot_importance(model)
plt.show()