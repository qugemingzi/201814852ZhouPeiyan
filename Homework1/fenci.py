# encoding=utf-8
import jieba

'''
将文本分词处理
测试分词工具jieba
'''

# 全模式
text = "我来到北京清华大学"
seg_list = jieba.cut(text, cut_all=True)
print ("[全模式]: ", "/ ".join(seg_list))
 
# 精确模式
seg_list = jieba.cut(text, cut_all=False)
print ("[精确模式]: ", "/ ".join(seg_list))
 
# 默认是精确模式
seg_list = jieba.cut(text)
print ("[默认模式]: ", "/ ".join(seg_list))
 
# 新词识别 “杭研”并没有在词典中,但是也被Viterbi算法识别出来了
seg_list = jieba.cut("他来到了网易杭研大厦") 
print ("[新词识别]: ", "/ ".join(seg_list))
 
# 搜索引擎模式
seg_list = jieba.cut_for_search(text) 
print ("[搜索引擎模式]: ", "/ ".join(seg_list))
