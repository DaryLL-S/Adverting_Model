# -*- coding: utf-8 -*-
# @Time    : 2021/12/22 16:30
# @Author  : Daryl
# @FileName: test.py
# @Software: PyCharm

import codecs
import csv
import logging
import re

import jieba.posseg as jieba
from gensim.models import fasttext

head = ['_key', 'username', 'location', 'postcount', 'likes', 'post', 'gender', 'identity', 'marriage', 'region',
        'risk_appetite', 'education', 'revenue', 'deposit', 'debt', 'intended_products', 'label']


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
    return result


def builtmodel():
    sens_list = []
    stopkey = [w.strip() for w in codecs.open('./data/stopWord.txt', 'r', encoding='utf-8').readlines()]
    with open("./data/process.csv", "w", encoding='utf-8', newline='') as wf:
        writer = csv.DictWriter(wf, fieldnames=head)
        writer.writeheader()
        with open("./data/full_data.csv", "r", encoding='utf-8', newline='') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                result = dataPrepos(row['post'], stopkey)
                # print('{}'.format(' '.join(seg_list)))
                # print(result)
                # 输出中间文件
                writer.writerow({'_key': row['_key'], 'username': row['username'], 'location': row['location'],
                                 'postcount': row['postcount'], 'likes': row['likes'], 'post': result})
                sens_list.append(result)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = fasttext.FastText(sens_list, min_count=1, sg=0)
    model.save("./result/model/fast_text_CBOW.model")
    model.wv.save_word2vec_format("./result/model/fast_text_CBOW.vector")
