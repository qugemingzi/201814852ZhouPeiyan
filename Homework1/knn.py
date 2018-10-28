# encoding=utf-8
import json
from collections import Counter

import numpy as np

'''
根据文档向量表示结合knn，将测试文档分类，检测成功率
'''

'''
加载训练文档向量表示
'''


def load_file_vector(file_vector_path):
    with open(file_vector_path, "r", errors="replace") as f:
        js_vec = f.read()
    file_vector = json.loads(js_vec)
    for filename in file_vector:
        file_vector[filename] = np.array(file_vector[filename])
    return file_vector


'''
加载测试文档向量表示
'''


def load_file_vector_testing(file_vector_testing_path):
    with open(file_vector_testing_path, "r", errors="replace") as f:
        js_vec = f.read()
    file_vector_testing = json.loads(js_vec)
    for filename in file_vector_testing:
        file_vector_testing[filename] = np.array(file_vector_testing[filename])
    return file_vector_testing


'''
使用knn方法，计算测试文档与训练文档的每篇文档cos相似度
进行分类，并计算成功率
'''


def knn(file_vector, file_vector_testing, k):
    classify = {}  # {"文档名": "分类", ...}
    classify_more = {}  # {"文档名": ["分类1", "分类2", "分类3"], ...}
    for file_test in file_vector_testing:
        vec_test = file_vector_testing[file_test]
        k_list = {}  # cos最大的k个分类
        for file_name in file_vector:
            k_list = compute_k(k_list, file_name, file_vector[file_name], vec_test, k)
        print("k_list is %s" % k_list)
        count_classify = {}  # 将k_list计数，其实Counter更好
        for fname in k_list:
            if fname[0:2] not in count_classify.keys():
                count_classify[fname[0:2]] = 1
            else:
                count_classify[fname[0:2]] += 1

        for cla in count_classify:
            if count_classify[cla] == max(count_classify.values()):
                classify[file_test] = cla
                break

        count_list3 = Counter(count_classify).most_common(3)
        count_list = []
        for i in range(len(count_list3)):
            count_list.append(count_list3[i][0])
        classify_more[file_test] = count_list

        print("file_test %s " % file_test)
        print("count_classify is %s " % count_classify)

    cla_right = 0
    for fcla in classify:
        if classify[fcla] == fcla[0:2]:
            # print(fcla[0:2])
            cla_right += 1
    print("采用k为 %s 的设置" % k)
    print("分类正确文档数目 %s, 全部测试文档数目 %s" % (cla_right, len(classify)))
    print("测试数据正确率为 %s" % (cla_right / len(classify)))

    cla_right3 = 0
    for fcla in classify_more:
        if fcla[0:2] in classify_more[fcla]:
            # print(fcla[0:2])
            cla_right3 += 1
    print("若在k为 %s 中，前三个能匹配上")
    print("模糊分类正确文档数目 %s, 全部测试文档数目 %s" % (cla_right3, len(classify_more)))
    print("模糊测试数据正确率为 %s" % (cla_right3 / len(classify_more)))


'''
计算向量间的cos值，并将最大的k个存入k_list中
'''


def compute_k(k_list, file_name, vec_file, vec_test, k):
    cos = np.dot(vec_file, vec_test)
    if len(k_list) < k:
        k_list[file_name] = cos
    else:
        if cos > min(k_list.values()):  # 替换
            for file in k_list:
                if k_list[file] == min(k_list.values()):
                    k_list.pop(file)
                    k_list[file_name] = cos
                    break
    return k_list


if __name__ == "__main__":
    file_vector_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileVector'
    file_vector_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileVectorTesting'

    print("开始加载file_vector!")
    file_vector = load_file_vector(file_vector_path)
    print("加载file_vector结束!")
    print("开始加载file_vector_testing!")
    file_vector_testing = load_file_vector_testing(file_vector_testing_path)
    print("加载file_vector_testing结束!")

    # k = 3
    k = 10
    print("开始测试knn, k为 %s!" % k)
    knn(file_vector, file_vector_testing, k)
    print("测试knn结束！")
