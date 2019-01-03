# encoding=utf-8
import json
import re

import numpy as np
from nltk.corpus import stopwords
from collections import Counter
import math

'''
测试各种函数，以及各种库，finally为了更改commit
'''

print("\'" in "I haven't hehe")
print(any(char.isdigit() for char in "sdcsc2sdvsv"))
print(any(char.isdigit() for char in "sdcscsdvsv"))
print(bool(re.search(r'\d', "sdcsc2sdvsv")))
print(bool(re.search(r'\d', "sdcscsdvsv")))
print(stopwords.words("english"))
print("sdc+s".isalpha())

corpus = [
    'this is the first document',
    'this is the second second document',
    'and the third one',
    'is this the first document'
]

word_list = []
for i in range(len(corpus)):
    word_list.append(corpus[i].split(' '))
print(word_list)

countlist = []
for i in range(len(word_list)):
    count = Counter(word_list[i])
    countlist.append(count)
print(countlist)


# word可以通过count得到，count可以通过countlist得到
# count[word]可以得到每个单词的词频， sum(count.values())得到整个句子的单词总数
def tf(word, count):
    return count[word] / sum(count.values())


# 统计的是含有该单词的句子数
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


# len(count_list)是指句子的总数，n_containing(word, count_list)是指含有该单词的句子的总数，加1是为了防止分母为0
def idf(word, count_list):
    return math.log(len(count_list) / (n_containing(word, count_list)))


# 将tf和idf相乘
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


for i, count in enumerate(countlist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, count, countlist) for word in count}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

wlist = ['a', 'b', 'c', 'a', 'a']
wlist2 = ['a', 'b', 'b', 'b', 'b']
list = {"01": Counter(wlist), "02": Counter(wlist2)}
print("c" in list["01"].keys())
print("c" in list["02"].keys())
print(list)
word = "c"
print(sum(1 for count in list.values() if word in count))

vec_length = np.linalg.norm((3, 4, 5), ord=2, axis=0, keepdims=True)
vec_norm = (3, 4, 5) / vec_length
print(vec_length)
print(vec_norm)
for i in range(len(vec_norm)):
    vec_norm[i] = round(vec_norm[i], 5)
print(vec_norm)
print(vec_norm.tolist())

dic = {
    'andy': {
        'age': 23,
        'city': 'beijing',
        'skill': 'python'
    },
    'william': {
        'age': 25,
        'city': 'shanghai',
        'skill': 'js'
    }
}

vec_list = [1]

js = json.dumps(dic)
file = open('D:\\test.txt', 'w')
file.write(js)
file.close()

file2 = open('D:\\test.txt', 'r')
js2 = file2.read()
dic2 = json.loads(js2)
print(dic2)
file2.close()

my_dic = {"01": 1, "02": 2}
print(2 in my_dic.values())
print("01" in my_dic.keys())
# print(my_dic["00"])

vec = np.array(vec_list)
for i in range(len(vec_list)):
    if vec_list[i] > 0.012:
        print(vec_list[i])
vec_len = np.linalg.norm(vec, ord=2, axis=0, keepdims=True)
print(vec_len)

print(np.dot((1, 2), (2, 4)))

file_vector_testing_path = \
    'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileVectorTesting'
with open(file_vector_testing_path, "r", errors="replace") as f_vec:
    js_vec = f_vec.read()
dict_vec = json.loads(js_vec)
for key in dict_vec:
    if key == "01_49960" or key == "01_54137" or key == "02_38984" or key == "04_61130" or \
            key == "06_68252" or key == "08_103461" or key == "20_84563":
        print("file name is %s " % key)
        print("vector is %s" % dict_vec[key])

file_vector_path = \
    'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\FileVector'
with open(file_vector_path, "r", errors="replace") as f_vec:
    js_vec = f_vec.read()
dict_vec = json.loads(js_vec)
for key in dict_vec:
    if key == "01_51159" or key == "02_38722" or key == "04_60508" or key == "09_103229" or \
            key == "12_15435" or key == "16_21430" or key == "20_84265":
        print("file name is %s " % key)
        print("vector is %s" % dict_vec[key])

sort_dict = {"a": 1, "b": 13, "ac": 5}
# sort_dict = sorted(sort_dict.values(), reverse=True)
sort_list = Counter(sort_dict).most_common(2)
for i in range(len(sort_list)):
    print(sort_list[i][0])
print(sort_dict)

count_classify = {"a": 1, "b": 13, "ac": 5}
count_classify = sorted(count_classify.values(), reverse=True)
cla_list = []
cla_count = 0
for cla in count_classify:
    if cla_count < 4:
        cla_list.append(cla)
    else:
        break
print(cla_list)
