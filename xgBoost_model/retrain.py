import numpy as np
import pandas as pd
import xgboost as xgb


import myW2V_model.index


def main():
    myW2V_model.index.main()
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
    data = df2.iloc[:, 3:16]
    target = df2.iloc[:, -1:]

    # 增量训练
    params_02 = {'process_type': 'update',
                 'updater': 'refresh',
                 'refresh_leaf': True}

    new_model = xgb.train(params_02, xgb.DMatrix(data, target), xgb_model=model)
    new_model.save_model('XGboost.model')
