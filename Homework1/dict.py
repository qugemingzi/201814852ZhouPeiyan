# encoding=utf-8
import json
import os
from collections import Counter
import jieba

'''
根据分词后的文档生成词典
根据词频（<10）删减词典
返回纯词典，倒排索引词典，词频最大统计
'''

'''
生成纯词典，包括每个词及它的词频
此处做一个处理：将词频<10的词省略了
training_set_path: 训练数据集路径
dict_path: 生成词典路径
'''


def makeDict(training_set_path, dict_path):
    print("开始构建词典！")
    word_dict = {}  # 训练数据根据词频生成的词典
    files = os.listdir(training_set_path)  # 得到文件夹下的所有文件名称

    for file in files:
        tr_ds_path = os.path.join(training_set_path, file)  # 处理单个文件的路径
        with open(tr_ds_path, "r", errors="replace") as f:
            txt = f.read()
        word_list = jieba.cut(txt, cut_all=False)  # 分词
        for item in word_list:
            if item not in word_dict:
                word_dict[item] = 1
            else:
                word_dict[item] += 1

    my_Dict = {}  # 我的词典 {"单词": "155" ...}
    with open(dict_path, "w", encoding="utf-8") as f2:
        for key in word_dict:
            if key.isalpha():
                # print(key, word_dict[key])
                if word_dict[key] < 10:
                    pass
                else:
                    my_Dict[key] = word_dict[key]
                    f2.write(key + ' ' + str(word_dict[key]) + '\n')
    print("词典构建结束！")

    return my_Dict


'''
生成倒排索引词典，词频最大统计
training_set_path: 训练数据集路径
file_max_number_path: 词频最大统计路径
dict_inverted_path: 倒排索引词典路径
my_Dict: 之前生成的词频词典
'''


def makeDictInverted(training_set_path, file_max_number_path, dict_inverted_path, my_Dict):
    print("开始构建倒排词典！")
    word_list = {}  # 不同文档的内容生成的字典, {"文档名": "["a", "b", ...] ..."}
    countlist = {}  # 所有文档的词频计数生成的字典，{"文档名": Counter('car': 12, ...), ...}
    my_Dict_Inverted = {}  # 我的词典 {"单词": {"文档名": 155, "文档名": 255 ...}, ...}
    file_Max_Number = {}  # 每个文档出现最多频率数的字典 {"文档名": 15, ...}
    files = os.listdir(training_set_path)  # 得到文件夹下的所有文件名称

    for file in files:
        tr_ds_path = os.path.join(training_set_path, file)  # 处理单个文件的路径
        with open(tr_ds_path, "r", errors="replace") as f:
            txt = f.read()
        temp = txt.split("\n")
        text = []
        for i in range(len(temp)):
            text.extend(temp[i].split(" "))
        word_list[file] = text

    for key in word_list:
        count = Counter(word_list[key])  # 每篇文档的词频统计
        countlist[key] = count
        file_Max_Number[key] = max(count.values())

    js_file = json.dumps(file_Max_Number)
    with open(file_max_number_path, "w", encoding="utf-8") as f1:
        f1.write(js_file)

    for key in my_Dict:
        inverted_list = {}  # 倒排索引字典 {"文档名": "155", "文档名": "255" ...}
        for filename in countlist:
            if key in countlist[filename].keys():
                inverted_list[filename] = countlist[filename][key]
        my_Dict_Inverted[key] = inverted_list

    js_dict = json.dumps(my_Dict_Inverted)
    with open(dict_inverted_path, "w", encoding="utf-8") as f2:
        f2.write(js_dict)
    print("倒排词典构建结束！")


if __name__ == "__main__":
    # training_set_path = \
    #     "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\c"
    # dict_path = \
    #     "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDict"
    training_set_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet-Divide'
    dict_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Dict'
    file_max_number_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileMax'
    dict_inverted_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\DictInverted'
    my_Dict = makeDict(training_set_path, dict_path)
    makeDictInverted(training_set_path, file_max_number_path, dict_inverted_path, my_Dict)

    testing_set_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TestingDataSet-Divide'
    file_max_number_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileMaxTesting'
    dict_inverted_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\DictInvertedTesting'
    makeDictInverted(testing_set_path, file_max_number_testing_path, dict_inverted_testing_path, my_Dict)
