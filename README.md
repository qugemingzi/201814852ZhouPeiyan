# 201814852ZhouPeiyan
# Data Mining course
# Homework 1: VSM and KNN
# 任务：
#   -预处理文本数据集，并且得到每个文本的VSM表示。
#   -实现KNN分类器，测试其在20Newsgroups上的效果。
#   -20%作为测试数据集，保证测试数据中各个类的文档均匀分布。
# Deadline: 2018.11.5,23:00

2018/10/16 20：42
  数据集分类工作，80%为训练数据集，20%为测试数据集。
  了解了os库，shutil库中的一些方法。
  问题：我把训练数据集和测试数据集整个存储所有的文件，但是这些文件夹中有命名相同的文件，需要在复制文件时重命名这些文件。
  我的解决方法是将某个文件夹下的某个文件以“文件夹编号”+“原文件名”命名。
  例如第五个文件夹（默认字典排序）的101666文件，其文件名为“05_101666”。
  着手做分词工作，简单了解了jieba。

2018/10/28 21：23
  之间没有及时更新，提交代码，以后需要记住。
  总体流程为
  {
    划分数据集为训练以及测试用；
    采用jieba和nltk分词，生成通过停用词，词频长度，字母限制，词频过小等限制的词频词典；
    根据词频词典生成倒排索引词典，词频最大统计，这样子以后就可以不访问原文档了；
    根据倒排索引词典，词频最大统计，结合tf-idf公式生成文本向量表示；
    根据文本向量表示，采用knn分类方法，设置不同的k值，观察方法分类成功率；
  }
