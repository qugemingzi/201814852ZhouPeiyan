# encoding=utf-8
import json
import os
from collections import Counter

'''
生成文档计数
training_set_path: 训练数据集路径
file_naive_bayes_path: 文档计数路径
'''


def makeFileCount(training_set_path, file_naive_bayes_path):
    print("开始构建文档计数！")
    word_list = {}  # 不同文档的内容生成的字典, {"文档名": "["a", "b", ...] ..."}
    countlist = {}  # 所有文档的词频计数生成的字典，{"文档名": Counter('car': 12, ...), ...}
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
        count.pop("")  # 去除""
        countlist[key] = count

    js_file = json.dumps(countlist)
    with open(file_naive_bayes_path, "w", encoding="utf-8") as f1:
        f1.write(js_file)

    print("构建文档计数结束！")
    return countlist


'''
生成合并后的文档计数
countlist: 文档计数字典 {"文档名": Counter('car': 12, ...), ...}
merge_naive_bayes_path: 合并后的文档计数路径
'''


def merge_file_count(countlist, merge_naive_bayes_path):
    print("开始构建合并后的文档计数！")
    merge_countlist = {}  # 合并所有文档的词频计数生成的字典，{"类别": Counter('car': 12, ...'zhoupeiyan': 5555), ...}
    count_num_list = {}  # 计算各个类别文档数目生成的字典，{"类别": 5555, ...}

    for file in countlist:
        if file[0:2] in count_num_list.keys():
            count_num_list[file[0:2]] += 1
        else:
            count_num_list[file[0:2]] = 1
    # for file in count_num_list:
    #     print("类别：%s, 数目：%s" % (file, count_num_list[file]))

    for file in countlist:
        if file[0:2] in merge_countlist.keys():
            merge_countlist[file[0:2]] += countlist[file]
        else:
            merge_countlist[file[0:2]] = countlist[file]

    for class_name in merge_countlist:
        merge_countlist[class_name]["zhoupeiyan"] = count_num_list[class_name]
    # for class_name in merge_countlist:
    #     if class_name == "01":
    #         print(merge_countlist[class_name])
    # print(len(merge_countlist))

    js_file = json.dumps(merge_countlist)
    with open(merge_naive_bayes_path, "w", encoding="utf-8") as f1:
        f1.write(js_file)

    print("合并后的构建文档计数结束！")
    return countlist


if __name__ == "__main__":
    training_set_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet-Divide'
    file_naive_bayes_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileNB'
    merge_naive_bayes_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\MergeFileNB'
    merge_count_naive_bayes_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\MergeCountFileNB'

    countlist = makeFileCount(training_set_path, file_naive_bayes_path)  # 文档词频计数
    merge_file_count(countlist, merge_naive_bayes_path)  # 生成合并后的文档词频计数
    for file in countlist:
        for word in countlist[file]:
            countlist[file][word] = 1
    merge_file_count(countlist, merge_count_naive_bayes_path)  # 生成合并后的文档篇数计数

    testing_set_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TestingDataSet-Divide'
    file_naive_bayes_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileNBTesting'

    makeFileCount(testing_set_path, file_naive_bayes_testing_path)  # 文档词频计数
