# encoding=utf-8
import os
import shutil

'''
处理数据集
将dataset分割成两部分，按照82比
80%一组为训练数据TrainingDataSet
20%一组为测试数据TestingDataSet
'''

'''
srcPath: 源文件夹路径
desPath: 目标文件夹路径
divide 将srcPath路径下的文件copy到desPath路径下
'''


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


'''
srcPath: 源文件夹路径
trainPath: 训练文件夹路径
testPath: 测试文件夹路径
divide_into 将srcPath路径下的80%文件copy到trainPath路径下，剩余20%copy到testPath中
'''


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
        divide_line = total_count * 0.8  # 80%作为分界线，前80%为训练数据集，后20%为测试数据集
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


if __name__ == "__main__":
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

    divide_into(srcPath, trainPath, testPath)
    total_count = 0
    train_count = 0
    test_count = 0
    for root, dirs, files in os.walk(srcPath, True):
        total_count += len(files)
    for root, dirs, files in os.walk(trainPath, True):
        train_count += len(files)
    for root, dirs, files in os.walk(testPath, True):
        test_count += len(files)
    print("数据集总文档数目 %s" % total_count)
    print("训练数据集文档数目 %s" % train_count)
    print("测试数据集文档数目 %s" % test_count)
    '''
    问题：copy时一些相同命名的文件被覆盖，导致文件数目减少
    解决：仔细检查后发现有很多文件名是相同的，将文件复制之后重命名，01_XXXX
    本来共18828个文件，trainDataSet共15059个文件，testDataSet共3759个文件
    '''
