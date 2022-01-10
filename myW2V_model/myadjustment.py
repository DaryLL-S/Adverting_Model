import pandas as pd
from gensim.models import FastText


def final_adjustment():
    model = FastText.load("result/model/fast_text_CBOW.model")
    data = pd.read_csv('./result/keys_word2vec.csv')
    keyList = data['keyword']
    resultList = []
    for i in keyList:
        result = model.wv.distance(i, '无')
        print(i, result)
        resultList.append(result)
    a = pd.DataFrame({"_key": data['_key'], "username": data['username'], "location": data['location'],
                      "postcount": data['postcount'], "likes": data['likes'], "keyword": resultList,
                      "gender": data['gender'], "identity": data['identity'], "marriage": data['marriage'],
                      "region": data['region'], "risk_appetite": data['risk_appetite'], "education": data['education'],
                      "revenue": data['revenue'], "deposit": data['deposit'], "debt": data['debt'],
                      "intended_products": data['intended_products'], "label": data['label']},
                     columns=['_key', 'username', 'location', 'postcount', 'likes', 'keyword', 'gender', 'identity',
                              'marriage', 'region', 'risk_appetite', 'education', 'revenue', 'deposit', 'debt',
                              'intended_products', 'label'])
    a = a.sort_values(by="_key", ascending=True)  # 排序
    a.to_csv("./result/final_result.csv", index=False)
