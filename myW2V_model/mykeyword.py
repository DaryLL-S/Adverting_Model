import codecs
import math
import os
import re

import gensim
import jieba.posseg as jieba
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


# 返回特征词向量
def getWordVecs(wordList, model):
    name = []
    vecs = []
    for word in wordList:
        word = word.replace('\n', '')
        try:
            if word in model:  # 模型中存在该词的向量表示
                name.append(word)
                vecs.append(model[word])
        except KeyError:
            continue
    a = pd.DataFrame(name, columns=['word'])
    b = pd.DataFrame(np.array(vecs, dtype='float'))
    return pd.concat([a, b], axis=1)


# 数据预处理操作：分词，去停用词，词性筛选
def dataPrepos(text, stopkey):
    text = re.sub(r"[^\u4e00-\u9fa5]", '', text)  # 去除非中文词语
    result = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'result', 'a', 'd']  # 定义选取的词性
    seg = jieba.lcut(text)  # 分词
    for i in seg:
        if i.word not in result and i.word not in stopkey and i.flag in pos:  # 去重 + 去停用词 + 词性筛选
            # print i.word
            result.append(i.word)
    if not result:
        result.append("无")
    return result


# 根据数据获取候选关键词词向量
def buildAllWordsVecs(data, stopkey, model):
    idList, abstractList = data['_key'], data['post']
    for index in range(len(idList)):
        id = idList[index]
        post_content = abstractList[index]
        result = dataPrepos(post_content, stopkey)  # 处理摘要
        # 获取候选关键词的词向量
        words = list(set(result))  # 数组元素去重,得到候选关键词列表
        wordvecs = getWordVecs(words, model)  # 获取候选关键词的词向量表示
        # 词向量写入csv文件，每个词400维
        data_vecs = pd.DataFrame(wordvecs)
        data_vecs.to_csv('result/vecs/wordvecs_' + str(id) + '.csv', index=False)
        print("document ", id, " well done.")


# 对词向量采用K-means聚类抽取TopK关键词
def getkeywords_kmeans(data, topK):
    words = data["word"]  # 词汇
    vecs = data.iloc[:, 1:]  # 向量表示
    kmeans = KMeans(n_clusters=1, random_state=10).fit(vecs)
    labels = kmeans.labels_  # 类别结果标签
    labels = pd.DataFrame(labels, columns=['label'])
    new_df = pd.concat([labels, vecs], axis=1)
    df_count_type = new_df.groupby('label').size()  # 各类别统计个数
    # print df_count_type
    vec_center = kmeans.cluster_centers_  # 聚类中心

    # 计算距离（相似性） 采用欧几里得距离（欧式距离）
    distances = []
    vec_words = np.array(vecs)  # 候选关键词向量，dataFrame转array
    vec_center = vec_center[0]  # 第一个类别聚类中心,本例只有一个类别
    length = len(vec_center)  # 向量维度
    for index in range(len(vec_words)):  # 候选关键词个数
        cur_wordvec = vec_words[index]  # 当前词语的词向量
        dis = 0  # 向量距离
        for index2 in range(length):
            dis += (vec_center[index2] - cur_wordvec[index2]) * (vec_center[index2] - cur_wordvec[index2])
        dis = math.sqrt(dis)
        distances.append(dis)
    distances = pd.DataFrame(distances, columns=['dis'])

    result = pd.concat([words, labels, distances], axis=1)  # 拼接词语与其对应中心点的距离
    result = result.sort_values(by="dis", ascending=True)  # 按照距离大小进行升序排序

    # 抽取排名前topK个词语作为文本关键词
    wordlist = np.array(result['word'])  # 选择词汇列并转成数组格式
    word_split = [wordlist[x] for x in range(0, topK)]  # 抽取前topK个词汇
    word_split = " ".join(word_split)
    return word_split


def word():
    # 读取数据集
    dataFile = 'data/full_data.csv'
    data = pd.read_csv(dataFile)

    # 停用词表
    stopkey = [w.strip() for w in codecs.open('data/stopWord.txt', 'r', encoding='utf-8').readlines()]

    # 词向量模型
    inp = 'result/model/fast_text_CBOW.vector'
    model = gensim.models.KeyedVectors.load_word2vec_format(inp, binary=False)
    buildAllWordsVecs(data, stopkey, model)

    uids, keys = [], []

    rootdir = "result/vecs"  # 词向量文件根目录
    fileList = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    fileList.sort(key=lambda x: int(x[9:-4]))
    # 遍历文件
    for i in range(len(fileList)):
        filename = fileList[i]
        path = os.path.join(rootdir, filename)
        print(path)
        if os.path.isfile(path):
            pdata = pd.read_csv(path, encoding='utf-8')  # 读取词向量文件数据
            keyword = getkeywords_kmeans(pdata, 1)  # 聚类算法得到当前文件的关键词
            # 根据文件名获得文章id以及标题
            (shortname, extension) = os.path.splitext(filename)  # 得到文件名和文件扩展名
            t = shortname.split("_")
            article_id = int(t[len(t) - 1])  # 获得文章id
            uids.append(article_id)
            keys.append(keyword)
    # 所有结果写入文件
    result = pd.DataFrame(
        {"_key": uids, "username": data['username'], "location": data['location'], "postcount": data['postcount'],
         "likes": data['likes'], "keyword": keys, "gender": data['gender'], "identity": data['identity'],
         "marriage": data['marriage'], "region": data['region'], "risk_appetite": data['risk_appetite'],
         "education": data['education'], "revenue": data['revenue'], "deposit": data['deposit'], "debt": data['debt'],
         "intended_products": data['intended_products'], "label": data['label']},
        columns=['_key', 'username', 'location', 'postcount', 'likes', 'keyword', 'gender',
                 'identity', 'marriage', 'region', 'risk_appetite', 'education', 'revenue',
                 'deposit', 'debt', 'intended_products', 'label'])
    print(uids)
    result = result.sort_values('_key')  # 排序
    result.to_csv("result/keys_word2vec.csv", index=False)


if __name__ == '__main__':
    word()