# coding=utf-8
import os
import jieba


'''
将文本分词处理
测试分词工具jieba
'''


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
分词.词性标注以及去停用词
dealpath：中文数据预处理文件的路径
savepath：中文数据预处理结果的保存路径
'''


def cutTxtWord(srcpath, respath):
    with open(srcpath, "r", encoding='utf-8') as f:
        txtlist = f.read()  # 读取待处理的文本
    words = jieba.cut(txtlist, cut_all=False)  # 分词结果
    cutresult = ""  # 单个文本：分词合并的结果
    for word in words:
        cutresult += word + " "
    standdata(cutresult, respath)


'''
分词.词性标注以及去停用词
stopwordspath： 停用词路径
read_folder_path ：中文数据预处理文件的路径
write_folder_path ：中文数据预处理结果的保存路径
filescount=300 #设置文件夹下文件最多多少个
'''


def cutFileWord(read_folder_path, write_folder_path):
    # 获取待处理根目录下的所有文件
    files = os.listdir(read_folder_path)  # 得到文件夹下的所有文件名称
    j = 1
    for file in files:
        if j > len(files):
            break
        srcpath = os.path.join(read_folder_path, file)  # 处理单个文件的路径
        with open(srcpath, "rb") as f:
            txtlist = f.read()
        words = jieba.cut(txtlist, cut_all=False)  # 分词结果
        cutresult = ""  # 单个文本：分词合并的结果
        for word in words:
            cutresult += word + " "
        respath = os.path.join(write_folder_path, file)
        standdata(cutresult, respath)
        j += 1


'''
标准化处理，去除空行，空白字符等。
flagresult:筛选过的结果
'''


def standdata(flagresult, respath):
    f2 = open(respath, "w", encoding='utf-8')
    f2.write(flagresult)
    f2.close()


# 测试单个文件
srcpath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\72052'
respath = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestFenci\\72052'

# 批量处理文件夹下的文件
srcfolder_path = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestDivideSrc\\a'
# srcfolder_path = '../Database/SogouC/FileNews/'
# 分词处理后保存根路径
resfolder_path = 'D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework1\\DataSet\\Test\\TestFenci\\fold'

# 中文语料预处理器
# cutTxtWord(srcpath, respath) # 单文本预处理器
cutFileWord(srcfolder_path, resfolder_path)  # 多文本预处理器
