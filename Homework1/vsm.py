# encoding=utf-8
import os

import jieba

'''
Vector Space Model处理
'''


def makeDict(training_set_path, dict_path):
    word_dict = {}  # 训练数据根据词频生成的词典
    files = os.listdir(training_set_path)  # 得到文件夹下的所有文件名称

    for file in files:
        tr_ds_path = os.path.join(training_set_path, file)  # 处理单个文件的路径
        with open(tr_ds_path, "r", errors="replace") as f:
            txt = f.read()
        word_list = jieba.cut(txt, cut_all=False)
        for item in word_list:
            if item.isalpha():
                if item not in word_dict:
                    word_dict[item] = 1
                else:
                    word_dict[item] += 1


    with open(dict_path, "w", encoding="utf-8") as f2:
        for key in word_dict:
            print(key, word_dict[key])
            if word_dict[key] < 10:
                pass
            else:
                f2.write(key + ' ' + str(word_dict[key]) + '\n')
    f2.close()


if __name__ == "__main__":
    # training_set_path = \
    #     "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\c"
    # dict_path = \
    #     "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDict"
    training_set_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet-Divide'
    dict_path = \
        'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Dict'
    makeDict(training_set_path, dict_path)
