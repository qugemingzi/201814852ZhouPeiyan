# encoding=utf-8
import json
import math

'''
通过朴素贝叶斯方法进行文本分类
merge_naive_bayes_path: 合并后的文档词频计数路径
merge_count_naive_bayes_path: 合并后的文档篇数计数路径
file_naive_bayes_testing_path：测试文档词频计数路径
mode：模型选择，0-多项式，1-伯努利，2-混合，3-反混合
'''


def nb(merge_naive_bayes_path, merge_count_naive_bayes_path, file_naive_bayes_testing_path, mode):
    with open(merge_naive_bayes_path, "r", errors="replace") as f1:
        js_merge_nb = f1.read()
    merge_nb = json.loads(js_merge_nb)

    with open(merge_count_naive_bayes_path, "r", errors="replace") as f2:
        js_merge_count_nb = f2.read()
    merge_count_nb = json.loads(js_merge_count_nb)

    with open(file_naive_bayes_testing_path, "r", errors="replace") as f3:
        js_file_nb_testing = f3.read()
    file_nb_testing = json.loads(js_file_nb_testing)

    if mode == 0:
        polynomial(merge_nb, file_nb_testing)
    elif mode == 1:
        bernoulli(merge_count_nb, file_nb_testing)
    elif mode == 2:
        combine(merge_nb, file_nb_testing)
    elif mode == 3:
        uncombine(merge_count_nb, file_nb_testing)
    else:
        print("模式选择错误！0-多项式，1-伯努利，2-混合，3-反混合")


def polynomial(merge_nb, file_nb_testing):
    total_number = 0  # 总训练文档数目
    for merge in merge_nb:
        total_number += merge_nb[merge]["zhoupeiyan"]  # 该类别训练文档数目

    classify = {}  # {"文档名": "分类", ...}
    for file in file_nb_testing:
        cla_file = ""
        cla_nb = 1
        for merge in merge_nb:
            v = merge_nb[merge]["zhoupeiyan"] / total_number  # P(Vj)
            result = math.log(v)  # 取对数减少计算
            # 平滑处理 Laplace技术
            fenmu = sum(merge_nb[merge].values()) - merge_nb[merge]["zhoupeiyan"] + sum(file_nb_testing[file].values())
            for word in file_nb_testing[file]:
                if word in merge_nb[merge].keys():
                    temp_result = (merge_nb[merge][word] + 1) / fenmu  # P(Xi|Vj)
                else:
                    temp_result = 1 / fenmu  # P(Xi|Vj)
                result += file_nb_testing[file][word] * math.log(temp_result)
            if cla_nb == 1 or result > cla_nb:
                cla_nb = result
                cla_file = merge
        classify[file] = cla_file
    print("采用polynomial的模式")
    evaluate(classify)


def bernoulli(merge_count_nb, file_nb_testing):
    total_number = 0  # 总训练文档数目
    for merge in merge_count_nb:
        total_number += merge_count_nb[merge]["zhoupeiyan"]  # 该类别训练文档数目

    classify = {}  # {"文档名": "分类", ...}
    for file in file_nb_testing:
        cla_file = ""
        cla_nb = 1
        for merge in merge_count_nb:
            v = merge_count_nb[merge]["zhoupeiyan"] / total_number  # P(Vj)
            result = math.log(v)  # 取对数减少计算
            # 平滑处理 Laplace技术
            fenmu = sum(merge_count_nb[merge].values()) - merge_count_nb[merge]["zhoupeiyan"] + len(merge_count_nb)
            for word in file_nb_testing[file]:
                if word in merge_count_nb[merge].keys():
                    temp_result = (merge_count_nb[merge][word] + 1) / fenmu  # P(Xi|Vj)
                else:
                    temp_result = 1 / fenmu  # P(Xi|Vj)
                result += math.log(temp_result)
            if cla_nb == 1 or result > cla_nb:
                cla_nb = result
                cla_file = merge
        classify[file] = cla_file
    print("采用bernoulli的模式")
    evaluate(classify)


def combine(merge_nb, file_nb_testing):
    total_number = 0  # 总训练文档数目
    for merge in merge_nb:
        total_number += merge_nb[merge]["zhoupeiyan"]  # 该类别训练文档数目

    classify = {}  # {"文档名": "分类", ...}
    for file in file_nb_testing:
        cla_file = ""
        cla_nb = 1
        for merge in merge_nb:
            v = merge_nb[merge]["zhoupeiyan"] / total_number  # P(Vj)
            result = math.log(v)  # 取对数减少计算
            # 平滑处理 Laplace技术
            fenmu = sum(merge_nb[merge].values()) - merge_nb[merge]["zhoupeiyan"] + sum(file_nb_testing[file].values())
            for word in file_nb_testing[file]:
                if word in merge_nb[merge].keys():
                    temp_result = (merge_nb[merge][word] + 1) / fenmu  # P(Xi|Vj)
                else:
                    temp_result = 1 / fenmu  # P(Xi|Vj)
                result += math.log(temp_result)
            if cla_nb == 1 or result > cla_nb:
                cla_nb = result
                cla_file = merge
        classify[file] = cla_file
    print("采用combine的模式")
    evaluate(classify)


def uncombine(merge_count_nb, file_nb_testing):
    total_number = 0  # 总训练文档数目
    for merge in merge_count_nb:
        total_number += merge_count_nb[merge]["zhoupeiyan"]  # 该类别训练文档数目

    classify = {}  # {"文档名": "分类", ...}
    for file in file_nb_testing:
        cla_file = ""
        cla_nb = 1
        for merge in merge_count_nb:
            v = merge_count_nb[merge]["zhoupeiyan"] / total_number  # P(Vj)
            result = math.log(v)  # 取对数减少计算
            # 平滑处理 Laplace技术
            fenmu = sum(merge_count_nb[merge].values()) - merge_count_nb[merge]["zhoupeiyan"] + len(merge_count_nb)
            for word in file_nb_testing[file]:
                if word in merge_count_nb[merge].keys():
                    temp_result = (merge_count_nb[merge][word] + 1) / fenmu  # P(Xi|Vj)
                else:
                    temp_result = 1 / fenmu  # P(Xi|Vj)
                result += file_nb_testing[file][word] * math.log(temp_result)
            if cla_nb == 1 or result > cla_nb:
                cla_nb = result
                cla_file = merge
        classify[file] = cla_file
    print("采用uncombine的模式")
    evaluate(classify)


'''
计算naive bayes方法的正确率
classify: 分类词典
'''


def evaluate(classify):
    cla_right = 0
    for fcla in classify:
        if classify[fcla] == fcla[0:2]:
            cla_right += 1
    print("分类正确文档数目 %s, 全部测试文档数目 %s" % (cla_right, len(classify)))
    print("测试数据正确率为 %s" % (cla_right / len(classify)))


if __name__ == "__main__":
    merge_naive_bayes_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\MergeFileNB'
    merge_count_naive_bayes_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\MergeCountFileNB'
    file_naive_bayes_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileNBTesting'

    for mode in range(4):  # 三种模型，0-多项式，1-伯努利，2-混合，3-反混合
        nb(merge_naive_bayes_path, merge_count_naive_bayes_path, file_naive_bayes_testing_path, mode)

