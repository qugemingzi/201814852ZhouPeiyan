# encoding=utf-8
import os
import shutil

'''
将dataset分割成两部分，按照2：8比
20%一组为训练数据TrainingDataSet
80%一组为测试数据TestingDataSet
'''


# divide 将srcPath路径下的文件copy到desPath路径下
def divide(srcPath, desPath):
    # 若源路径不存在
    if not os.path.exists(srcPath):
        print("srcPath does not exist!")
    # 若目标路径不存在
    if not os.path.exists(desPath):
        print("desPath does not exist!")
    for root, dirs, files in os.walk(srcPath, True):
        count = 0
        for eachfile in files:
            print("files count is: %s" % count)
            count += 1
            shutil.copy(os.path.join(root, eachfile), desPath)


# divide 将srcPath路径下的20%文件copy到trainPath路径下，剩余80%copy到testPath中
def divide_into(srcPath, trainPath, testPath):
    # 若源路径不存在
    if not os.path.exists(srcPath):
        print("srcPath does not exist!")
    # 若训练集路径不存在
    if not os.path.exists(trainPath):
        print("trainPath does not exist!")
    # 若测试集路径不存在
    if not os.path.exists(testPath):
        print("testPath does not exist!")
    train_count = 0  # trainDataSet文件数量
    test_count = 0  # testDataSet文件数量
    dir_count = -1  # 文件编号
    for root, dirs, files in os.walk(srcPath, True):
        total_count = len(files)  # 该文件夹下文件总数目
        divide_line = total_count * 0.2  # 20%作为分界线，前20%为训练数据集，后80%为测试数据集
        dir_count += 1
        count = 0
        for eachfile in files:
            # print("files count is: %s" % count)
            if count < divide_line:  # 进入训练数据集
                train_count += 1
                print("count is %s, it is lower than %s!" % (count, divide_line))
                if dir_count < 10:
                    newfile = "0" + str(dir_count) + "_" + eachfile  # 重命名后的文件名
                else:
                    newfile = str(dir_count) + "_" + eachfile  # 同上
                shutil.copy(os.path.join(root, eachfile), os.path.join(trainPath, newfile))  # 复制并重命名
            else:  # 进入测试数据集
                test_count += 1
                print("count is %s, it is higher than %s!" % (count, divide_line))
                if dir_count < 10:
                    newfile = "0" + str(dir_count) + "_" + eachfile  # 重命名后的文件名
                else:
                    newfile = str(dir_count) + "_" + eachfile  # 同上
                shutil.copy(os.path.join(root, eachfile), os.path.join(testPath, newfile))  # 复制并重命名
            count += 1
    print("train_count is %s, while test_count is %s" % (train_count, test_count))


'''
This code is for testing!!!
srcPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc'
desPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideDes'
trainPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideTrain'
testPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideTest'
divide(srcPath, desPath)
divide_into(srcPath,trainPath, testPath)
'''

srcPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\20news-18828'
trainPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TrainingDataSet'
testPath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\TestingDataSet'
print("We will divide DataSet into two part, which one is for training, another is for testing!")
divide_into(srcPath,trainPath, testPath)
total_count = 0
train_count = 0
test_count = 0
for root, dirs, files in os.walk(srcPath, True):
    total_count += len(files)
for root, dirs, files in os.walk(trainPath, True):
    train_count += len(files)
for root, dirs, files in os.walk(testPath, True):
    test_count += len(files)
print(total_count)
print(train_count)
print(test_count)
'''
问题：copy时一些相同命名的文件被覆盖，导致文件数目减少
解决：仔细检查后发现有很多文件名是相同的，将文件复制之后重命名，01_XXXX
本来共18828个文件，trainDataSet共3772个文件，testDataSet共15056个文件
'''




