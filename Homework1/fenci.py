# coding=utf-8
import os
import jieba
import nltk
from nltk.corpus import stopwords
import re

'''
数据集分词，并做预处理
采用分词工具jieba
去掉nltk中的停用词stopwards
去掉非字母单词
单词小写
单词长度限制 > 1 and < 18
'''

# 测试jieba工具
def testjieba():
    # 全模式
    text = "我来到北京清华大学"
    seg_list = jieba.cut(text, cut_all=True)
    print("[全模式]: ", "/ ".join(seg_list))

    # 精确模式
    seg_list = jieba.cut(text, cut_all=False)
    print("[精确模式]: ", "/ ".join(seg_list))

    # 默认是精确模式
    seg_list = jieba.cut(text)
    print("[默认模式]: ", "/ ".join(seg_list))

    # 新词识别 “杭研”并没有在词典中,但是也被Viterbi算法识别出来了
    seg_list = jieba.cut("他来到了网易杭研大厦")
    print("[新词识别]: ", "/ ".join(seg_list))

    # 搜索引擎模式
    seg_list = jieba.cut_for_search(text)
    print("[搜索引擎模式]: ", "/ ".join(seg_list))


'''
通过nltk构建stpwords
'''


def getStpwords():
    stpwords = stopwords.words("english")
    stpwords.append([' ', '\t', '\n'])
    return stpwords


'''
分词.词性标注以及去停用词
stpwords: 停用词表
srcpath: 数据预处理文件的路径
respath: 数据预处理结果的保存路径
处理一个文档
'''


def cutTxtWord(srcpath, respath, stpwords):
    with open(srcpath, "r", encoding='utf-8') as f:
        txtlist = f.read()  # 读取待处理的文本
    porter = nltk.PorterStemmer()  # 词干分析
    splitter = re.compile('[^a-zA-Z]')  # 去除非字母字符，形成分隔
    words = [porter.stem(word.lower()) for word in splitter.split(txtlist)
             if len(word) > 0 and word.lower() not in stpwords]
    standdata(words, respath)


'''
分词.词性标注以及去停用词
stpwords： 停用词表
read_folder_path: 数据预处理文件的路径
write_folder_path: 数据预处理结果的保存路径
处理一个文件夹下的所有文档
'''


def cutFileWord(read_folder_path, write_folder_path, stpwords):
    # 获取待处理根目录下的所有文件
    files = os.listdir(read_folder_path)  # 得到文件夹下的所有文件名称
    for file in files:
        srcpath = os.path.join(read_folder_path, file)  # 处理单个文件的路径
        with open(srcpath, "r", errors="replace") as f:
            txtlist = f.read()
        porter = nltk.PorterStemmer()  # 词干分析
        splitter = re.compile('[^a-zA-Z]')  # 去除非字母字符，形成分隔
        words = [porter.stem(word.lower()) for word in splitter.split(txtlist)
                 if len(word) > 0 and word.lower() not in stpwords]
        standdata(words, os.path.join(write_folder_path, file))


'''
标准化处理，去除空行，空白字符等。
flagresult: 筛选过的结果
respath: 保存路径
'''


def standdata(flagresult, respath):
    f2 = open(respath, "w", encoding='utf-8')
    flag = 0
    for item in flagresult:
        # 再次筛选单词
        if len(item) > 2 and len(item) < 18 and item.isalpha():
            # 分词后每20个词一行写入文档
            if flag < 20:
                f2.write(item + " ")
            else:
                f2.write("\n")
                flag -= 20
            flag += 1
        else:
            pass
    f2.close()


if __name__ == '__main__':
    # 获取stpwords
    stpwords = getStpwords()

    # 测试单个文件
    Test_srcpath = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\72052'
    Test_respath = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestFenci\\72052'

    # 批量处理文件夹下的文件
    Test_srcfolder_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\c'
    # 分词处理后保存根路径
    Test_resfolder_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestFenci\\fold'

    # 语料预处理器
    # cutTxtWord(Test_srcpath, Test_respath, stpwords) # 单文本预处理器
    # cutFileWord(Test_srcfolder_path, Test_resfolder_path, stpwords)  # 多文本预处理器

    Training_srcfolder_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet'
    Training_resfolder_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet-Divide'
    Testing_srcfolder_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TestingDataSet'
    Testing_resfolder_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TestingDataSet-Divide'

    print("训练数据开始分词！")
    cutFileWord(Training_srcfolder_path, Training_resfolder_path, stpwords)  # 处理训练数据
    print("训练数据已经分词完毕！")
    print("测试数据开始分词！")
    cutFileWord(Testing_srcfolder_path, Testing_resfolder_path, stpwords)  # 处理测试数据
    print("测试数据已经分词完毕！")
