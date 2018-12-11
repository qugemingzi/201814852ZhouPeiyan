# 201814852ZhouPeiyan
# Data Mining course
# Homework 1: VSM and KNN
任务：

   -预处理文本数据集，并且得到每个文本的VSM表示。
   
   -实现KNN分类器，测试其在20Newsgroups上的效果。
   
   -20%作为测试数据集，保证测试数据中各个类的文档均匀分布。
   
# Deadline: 2018.11.5,23:00

2018/10/16 20：42

  数据集分类工作，80%为训练数据集，20%为测试数据集。
  
  了解了os库，shutil库中的一些方法。
  
  问题：训练数据集和测试数据集都单独作为一个文件夹，其下是所有文档，但是这些文件夹中有命名相同的文件，需要在复制文件时重命名这些文件。
  
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
    
    根据文本向量表示，采用knn分类方法，设置不同的k值，观察方法分类成功率。
    
  }
  
# Homework 2: NBC
任务：

   -实现朴素贝叶斯分类器，测试其在 20 Newsgroups 数据集上的效果。
   
   -比较不同三种计算模型的优劣，观察分类效果。
   
# Deadline: 2018.11.25,23:00

2018/12/11 14：33
  
  之前提交Homework2的时候忘记更新README了，思路步骤见实验报告。
  
# Homework 3: Clustering with sklearn
任务：

   -测试sklearn中以下聚类算法在tweets数据集上的聚类效果。
   
   -使用NMI(Normalized Mutual Information)作为评价指标。
   
# Deadline: 2018.12.25,23:00 (由于尹老师不忍心看我们备考别的科目，延长deadline且此为最后一个小作业/笑哭)

2018/12/11 14：50

  The Tweets dataset is in format of JSON like follows:
  
  -{"text": "centrepoint winter white gala london", "cluster": 65}
  
  -{"text": "mourinho seek killer instinct", "cluster": 96}
  
  -{"text": "roundup golden globe won seduced johansson voice", "cluster": 72}
  
  -{"text": "travel disruption mount storm cold air sweep south florida", "cluster": 140}

