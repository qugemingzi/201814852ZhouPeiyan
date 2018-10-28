# encoding=utf-8
import json
import math

import numpy as np

'''
根据倒排索引词典和词频最大统计生成文档向量表示
自定义tf-idf求解公式
返回文档向量表示
'''

'''
根据倒排索引词典和词频最大统计生成文档向量表示
dict_inverted_path: 倒排索引词典路径
file_max_number_path: 词频最大统计路径
file_vector_path: 文档向量表示路径
'''


def dealFile(dict_inverted_path, file_max_number_path, file_vector_path):
    with open(dict_inverted_path, "r", errors="replace") as f:
        js_dict = f.read()
    dict_inverted = json.loads(js_dict)  # 我的词典 {"单词": {"文档名": 155, "文档名": 255 ...}, ...}
    print("词典大小 %s" % len(dict_inverted))

    with open(file_max_number_path, "r", errors="replace") as f2:
        js_file = f2.read()
    file_max_number = json.loads(js_file)  # 每个文档出现最多频率数的字典 {"文档名": 15, ...}
    print("文档个数 %s" % len(file_max_number))

    result = {}  # 每个文档vector表示 {"文档名": (0.01, 0.05,...), ...}
    numbers_of_files = len(file_max_number)
    for file_name in file_max_number:
        scores = []
        for word in dict_inverted:
            numbers_containing_words = len(dict_inverted[word])
            if file_name in dict_inverted[word]:
                scores.append(
                    tfidf(file_max_number[file_name], dict_inverted[word][file_name], numbers_containing_words,
                          numbers_of_files))
            else:
                scores.append(tfidf(file_max_number[file_name], 0, numbers_containing_words, numbers_of_files))
        vec_before = np.array(scores)  # list转array
        vec_length = np.linalg.norm(vec_before, ord=2, axis=0, keepdims=True)  # 模长
        vec_norm = vec_before / vec_length  # 规范化，向量模长为1
        # for i in range(len(vec_norm)):
        #     vec_norm[i] = round(vec_norm[i], 5)
        result[file_name] = vec_norm.tolist()

    js_vec = json.dumps(result)
    with open(file_vector_path, "w", encoding="utf-8") as f3:
        f3.write(js_vec)

    return result


'''
将tf和idf相乘
'''


def tfidf(file_max_number, file_number, numbers_containing_words, numbers_of_files):
    score = tf(file_max_number, file_number) * idf(numbers_containing_words, numbers_of_files)
    return score


'''
tf公式 = (文章中某单词词频 / 文章中词频最大数)
'''


def tf(file_max_number, file_number):
    return file_number / file_max_number


'''
idf公式 = log[(1 + 文档数) / (1 + 包含该单词文档数)]
加1避免测试文档不包含某个单词
'''


def idf(numbers_containing_words, numbers_of_files):
    return math.log((1 + numbers_of_files) / (1 + numbers_containing_words))


if __name__ == "__main__":
    dict_inverted_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\DictInverted'
    file_max_number_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileMax'
    file_vector_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileVector'

    dict_inverted_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\DictInvertedTesting'
    file_max_number_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileMaxTesting'
    file_vector_testing_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileVectorTesting'

    print("开始根据tf-idf计算文档向量!")
    Result = dealFile(dict_inverted_path, file_max_number_path, file_vector_path)  # Result为包含文件名和每个文件向量的字典
    print("共计算 %s 篇训练文档的向量！" % len(Result))

    ResultTesting = dealFile(dict_inverted_testing_path, file_max_number_testing_path, file_vector_testing_path)
    print("共计算 %s 篇测试文档的向量！" % len(ResultTesting))
    print("文档向量计算结束!")
