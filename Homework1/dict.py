# encoding=utf-8
import math
import os
from collections import Counter

import jieba
import numpy as np

'''
根据分词后的文档生成词典
根据词频（>=10）删减词典
返回词典
'''


def makeDict(training_set_path, dict_path):
    print("开始构建词典！")
    word_dict = {}  # 训练数据根据词频生成的词典
    files = os.listdir(training_set_path)  # 得到文件夹下的所有文件名称

    for file in files:
        tr_ds_path = os.path.join(training_set_path, file)  # 处理单个文件的路径
        with open(tr_ds_path, "r", errors="replace") as f:
            txt = f.read()
        word_list = jieba.cut(txt, cut_all=False)
        for item in word_list:
            if item not in word_dict:
                word_dict[item] = 1
            else:
                word_dict[item] += 1
    my_Dict = {}  # 我的词典 {"单词": "155" ...}
    # with open(dict_path, "w", encoding="utf-8") as f2:
    for key in word_dict:
        if key.isalpha():
            # print(key, word_dict[key])
            if word_dict[key] < 10:
                pass
            else:
                my_Dict[key] = word_dict[key]
                # f2.write(key + ' ' + str(word_dict[key]) + '\n')
    # f2.close()
    print("词典构建结束！")
    return my_Dict


def makeDictInverted(training_set_path, dict_inverted_path, my_Dict):
    pass


def dealFile(src_path, res_path, dict):
    # 获取待处理根目录下的所有文件
    files = os.listdir(src_path)  # 得到文件夹下的所有文件名称

    word_list = {}  # 不同文档的内容生成的字典, {"文档名": "["a", "b", ...] ..."}
    countlist = {}  # 所有文档的词频计数生成的字典，{"文档名": Counter('car': 12, ...), ...}
    result = {}  # 结果词典
    for file in files:
        file_path = os.path.join(src_path, file)
        with open(file_path, "r", errors="replace") as f:
            txt = f.read()
        temp = txt.split("\n")
        text = []
        for i in range(len(temp)):
            text.extend(temp[i].split(" "))
        word_list[file] = text

    for key in word_list:
        count = Counter(word_list[key])  # 每篇文档的词频统计
        countlist[key] = count
    # print(len(countlist))
    # print(countlist["101551"])

    for key in countlist:
        # key is file name
        scores = [tfidf(word, countlist[key], countlist) for word in dict.keys()]
        vec_before = np.array(scores)
        vec_length = np.linalg.norm(vec_before, ord=2, axis=0, keepdims=True)
        vec_norm = vec_before / vec_length
        for i in range(len(vec_norm)):
            vec_norm[i] = round(vec_norm[i], 5)
        result[key] = vec_norm.tolist()

    print("计算tf-idf完毕!")
    with open(res_path, "w", encoding="utf-8") as f2:
        for key in result:
            f2.write(key + " " + str(result[key]) + "\n")
    f2.close()
    return result


# word可以通过count得到，count可以通过countlist得到
# count[word]可以得到每个单词的词频， max(count.values())得到整个句子的词频最大数
def tf(word, count):
    return (1 + count[word] / max(count.values())) / 2


# 统计的是含有该单词的句子数
def n_containing(word, count_list):
    return sum(1 for count in count_list.values() if word in count)


# len(count_list)是指句子的总数，n_containing(word, count_list)是指含有该单词的句子的总数
def idf(word, count_list):
    # if word == "subject":
        # print("length: %s" % len(count_list))
        # print("containing: %s" % (1 + n_containing(word, count_list)))
    return math.log(len(count_list) / n_containing(word, count_list))


# 将tf和idf相乘
def tfidf(word, count, count_list):
    # if word == "subject":
    #     print("tf: %f" % tf(word, count))
    #     print("idf: %f" % idf(word, count_list))
    score = tf(word, count) * idf(word, count_list)
    return round(score, 5)


if __name__ == "__main__":
    # training_set_path = \
    #     "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\c"
    # dict_path = \
    #     "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDict"
    training_set_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet-Divide'
    dict_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Dict'
    dict_inverted_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\DictInverted'
    # my_Dict = {}
    my_Dict = makeDict(training_set_path, dict_path)
    my_Dict_Inverted = makeDictInverted(training_set_path, dict_inverted_path, my_Dict)

    # src_path = \
    #     'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestFenci\\fold'
    # res_path = \
    #     'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestFenci\\result'
    src_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet-Divide'
    res_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Result'
    # print("开始计算文档向量和tf-idf!")
    # Result = dealFile(src_path, res_path, my_Dict)  # Result为包含文件名和每个文件向量的字典
    # print(len(Result))
