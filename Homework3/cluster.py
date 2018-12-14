# encoding=utf-8
import jieba
import json
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import Birch



def preProcess(DatasetPath):
    text_list = []
    clu_list = []
    with open(DatasetPath, "r", errors="replace") as f:
        i = 0  # 标记每条文本
        for line in f:
            js_tweets = line
            tweets = json.loads(js_tweets)
            for key in tweets:
                if key == "text":
                    text_list.append(tweets[key])
                elif key == "cluster":
                    cluster = int(tweets[key])
                    clu_list.append(cluster)
            i+=1
            
    return text_list, clu_list


def jieba_tokenize(text):
    return jieba.cut(text)
 

def tfidf(text_list):
    tfidf_vectorizer = TfidfVectorizer(tokenizer=jieba_tokenize, lowercase=True)
    '''
    tokenizer: 指定分词函数
    '''
    # 需要进行聚类的文本集
    tfidf_matrix = tfidf_vectorizer.fit_transform(text_list)
    
    return tfidf_matrix


def count(text_list):
    count_vectorizer = CountVectorizer(tokenizer=jieba_tokenize, lowercase=True)
    '''
    tokenizer: 指定分词函数
    '''
    # 需要进行聚类的文本集
    count_matrix = count_vectorizer.fit_transform(text_list)
    
    return count_matrix


def kmeans(tfidf_matrix, num_clusters):
    # num_clusters = 75
    km_cluster = KMeans(n_clusters=num_clusters, max_iter=300, n_init=10, init='k-means++')
    '''
    n_clusters: 指定K的值
    max_iter: 对于单次初始值计算的最大迭代次数
    n_init: 重新选择初始值的次数
    init: 制定初始值选择的算法
    n_jobs: 进程个数，为-1的时候是指默认跑满CPU
    '''
    # 返回各自文本的所被分配到的类索引
    result = km_cluster.fit_predict(tfidf_matrix)

    return result


def affinity_propagation(tfidf_matrix):
    ap_cluster = AffinityPropagation()
    '''
    damping: 衰减系数，默认为 0.5
    convergence_iter: 迭代次后聚类中心没有变化，算法结束，默认为15
    max_iter: 最大迭代次数，默认200
    copy: 是否在元数据上进行计算，默认True，在复制后的数据上进行计算
    preference: S的对角线上的值
    affinity: S矩阵（相似度），默认为euclidean（欧氏距离）矩阵
    '''
    # 返回各自文本的所被分配到的类索引
    result = ap_cluster.fit_predict(tfidf_matrix)

    return result


def mean_shift(tfidf_matrix):
    bw = estimate_bandwidth(tfidf_matrix.todense(), quantile=0.2, n_samples=500)
    ms_cluster = MeanShift(bandwidth=bw, bin_seeding=True)
    '''
    bandwidth: float，高斯核函数的带宽，如果没有给定，则使用sklearn.cluster.estimate_bandwidth 自动估计带宽
    seeds: array, 我理解的 seeds 是初始化的质心，如果为 None 并且 bin_seeding=True，就用 clustering.get_bin_seeds 计算得到
    bin_seeding: boolean，在没有设置 seeds 时起作用，
                如果 bin_seeding=True，就用 clustering.get_bin_seeds 计算得到质心，
                如果 bin_seeding=False，则设置所有点为质心
    min_bin_freq: int，clustering.get_bin_seeds 的参数，设置的最少质心个数
    '''
    # 返回各自文本的所被分配到的类索引
    result = ms_cluster.fit_predict(tfidf_matrix.todense())

    return result


def spectral_clustering(tfidf_matrix, num_clusters, option, num_neighbors):
    if option == 1:
        sc_cluster = SpectralClustering(affinity='rbf', n_clusters=num_clusters)
    elif option == 2:
        sc_cluster = SpectralClustering(affinity='nearest_neighbors', n_clusters=num_clusters, n_neighbors=num_neighbors)  
    '''
    n_clusters: 代表我们在对谱聚类切图时降维到的维数，同时也是最后一步聚类算法聚类到的维数。
                也就是说scikit-learn中的谱聚类对这两个参数统一到了一起。简化了调参的参数个数。
                虽然这个值是可选的，但是一般还是推荐调参选择最优参数。
    affinity: 也就是我们的相似矩阵的建立方式。可以选择的方式有三类，第一类是 'nearest_neighbors'即K邻近法。
                第二类是'precomputed'即自定义相似矩阵。第三类是全连接法，可以使用各种核函数来定义相似矩阵，还可以自定义核函数。
                最常用的是内置高斯核函数'rbf'。其他比较流行的核函数有‘linear’即线性核函数, ‘poly’即多项式核函数, 
                ‘sigmoid’即sigmoid核函数。如果选择了这些核函数， 对应的核函数参数在后面有单独的参数需要调。
                affinity默认是高斯核'rbf'。一般来说，相似矩阵推荐使用默认的高斯核函数。
    gamma: 如果我们在affinity参数使用了多项式核函数 'poly'，高斯核函数‘rbf’, 或者'sigmoid'核函数，那么我们就需要对这个参数进行调参。
    n_neighbors: 如果我们affinity参数指定为'nearest_neighbors'即K邻近法，则我们可以通过这个参数指定KNN算法的K的个数。
                默认是10.我们需要根据样本的分布对这个参数进行调参。如果我们affinity不使用'nearest_neighbors'，则无需理会这个参数。
    n_init: 即使用K-Means时用不同的初始值组合跑K-Means聚类的次数，这个和K-Means类里面n_init的意义完全相同，
            默认是10，一般使用默认值就可以。如果你的n_clusters值较大，则可以适当增大这个值。
    '''
    # 返回各自文本的所被分配到的类索引
    result = sc_cluster.fit_predict(tfidf_matrix)

    return result


def agglomerative_clustering(tfidf_matrix, num_clusters, option):
    ac_cluster = AgglomerativeClustering(linkage=option, n_clusters=num_clusters)
    '''
    n_clusters: 一个整数，指定分类簇的数量
    connectivity: 一个数组或者可调用对象或者None，用于指定连接矩阵
    affinity: 一个字符串或者可调用对象，用于计算距离。可以为: 'euclidean', 'l1', 'l2', 'mantattan', 'cosine', 'precomputed',
            如果linkage='ward'，则affinity必须为'euclidean'
    linkage: 一个字符串，用于指定链接算法 
            'single': 单链接single-linkage，采用dmindmin
            'complete': 全链接complete-linkage算法，采用dmaxdmax
            'average': 均连接average-linkage算法，采用davg
            'ward': 最小化被合并的clusters的方差
    '''
    # 返回各自文本的所被分配到的类索引
    result = ac_cluster.fit_predict(tfidf_matrix.todense())

    return result


def dbscan(tfidf_matrix):
    db_cluster = DBSCAN(eps=1, min_samples=1)
    '''
    eps: DBSCAN算法参数，即我们的ϵ-邻域的距离阈值，和样本距离超过ϵ的样本点不在ϵ-邻域内。默认值是0.5,
        一般需要通过在多组值里面选择一个合适的阈值。eps过大，则更多的点会落在核心对象的ϵ-邻域，此时我们的类别数可能会减少，
        本来不应该是一类的样本也会被划为一类。反之则类别数可能会增大，本来是一类的样本却被划分开。
    min_samples: DBSCAN算法参数，即样本点要成为核心对象所需要的ϵ-邻域的样本数阈值。默认值是5,
        一般需要通过在多组值里面选择一个合适的阈值。通常和eps一起调参。在eps一定的情况下，min_samples过大，则核心对象会过少，
        此时簇内部分本来是一类的样本可能会被标为噪音点，类别数也会变多。反之min_samples过小，则会产生大量的核心对象，导致类别数过少。
    '''
    # 返回各自文本的所被分配到的类索引
    result = db_cluster.fit_predict(tfidf_matrix)

    return result


def birch(tfidf_matrix):
    b_cluster = Birch(n_clusters=90, threshold=0.7)
    '''
    threshold: 即叶节点每个CF的最大样本半径阈值T，它决定了每个CF里所有样本形成的超球体的半径阈值。
            一般来说threshold越小，则CF Tree的建立阶段的规模会越大，即BIRCH算法第一阶段所花的时间和内存会越多。
            但是选择多大以达到聚类效果则需要通过调参决定。默认值是0.5.如果样本的方差较大，则一般需要增大这个默认值。
    branching_factor: 即CF Tree内部节点的最大CF数B，以及叶子节点的最大CF数L。这里scikit-learn对这两个参数进行了统一取值。
            也就是说，branching_factor决定了CF Tree里所有节点的最大CF数。默认是50。如果样本量非常大，比如大于10万，则一般需要增大这个默认值。
            选择多大的branching_factor以达到聚类效果则需要通过和threshold一起调参决定
    n_clusters: 即类别数K，在BIRCH算法是可选的，如果类别数非常多，我们也没有先验知识，则一般输入None，此时BIRCH算法第4阶段不会运行。
            但是如果我们有类别的先验知识，则推荐输入这个可选的类别值。默认是3，即最终聚为3类。
    '''
    # 返回各自文本的所被分配到的类索引
    result = b_cluster.fit_predict(tfidf_matrix)

    return result


def evaluate(result, clu_list):
    eva = nmi(clu_list, result, average_method='arithmetic')
#    print("采用NMI评测方法，预测正确率为：%s" % eva)
    # print(nmi(clu_list, result, average_method='warn'))
    return eva


def clustering(mode, tfidf_matrix, count_matrix, clu_list):
    best_eva = 0
    best_k = 0
    best_n = 0
    if mode == 1:
        for i in range(1, len(Counter(clu_list)), 2):
            result = kmeans(tfidf_matrix, (i+1))# i+1
#            print("num_cluster为%s时" % (i+1))# i+1
            eva = evaluate(result, clu_list)
            if eva > best_eva:
                best_eva = eva
                best_k = i + 1
        print("选择mode为1(K-means)时，采用NMI评测方法，best_k为%s时正确率最高，为%s" % (best_k, best_eva))
    elif mode == 2:
        result = affinity_propagation(tfidf_matrix)
        best_eva = evaluate(result, clu_list)
        print("选择mode为2(AffinityPropagation)时，采用NMI评测方法，正确率为%s" % best_eva)
    elif mode == 3:
        result = mean_shift(count_matrix)
        best_eva = evaluate(result, clu_list)
        print("选择mode为3(MeanShift)时，采用NMI评测方法，正确率为%s" % best_eva)
    elif mode == 4:
        option = 0
        for i in range(1, len(Counter(clu_list)), 3):
            # affinity设置为默认高斯核函数,'rbf'
            result = spectral_clustering(tfidf_matrix, (i+1), 1, 0)# i+1
#            print("num_cluster为%s时" % (i+1))# i+1
            eva = evaluate(result, clu_list)
            if eva > best_eva:
                best_eva = eva
                best_k = i + 1
                option = 1
        if option == 1:
            print("选择mode为4(SpectralClustering)时，affinity为高斯核函数'rbf'")
            print("采用NMI评测方法，best_k为%s时正确率最高为%s" % (best_k, best_eva))
        
        for i in range(10, 70, 3):
            # affinity设置为K邻近法,'nearest_neighbors'
            for j in range(5, 20):
                result = spectral_clustering(tfidf_matrix, (i+1), 2, (j+1))# i+1, j+1
#                print("num_cluster为%s, num_neighbors为%s时" % ((i+1), (j+1)))# i+1, j+1
                eva = evaluate(result, clu_list)
                if eva > best_eva:
                    best_eva = eva
                    best_k = i + 1
                    best_n = j + 1
                    option = 2
        if option == 2:
            print("选择mode为4(SpectralClustering)时，affinity为K邻近法'nearest_neighbors'")
            print("采用NMI评测方法，best_k为%s, besk_n为%s时正确率最高为%s" % (best_k, best_n, best_eva))
    elif mode == 5:
        # 运行时间很长，正确率如顺序 s-a-c-w
        best_option = ''
        for option in ('single', 'average', 'complete', 'ward'):
            best_eva = 0
            for i in range(20, len(Counter(clu_list)), 5):
                result = agglomerative_clustering(count_matrix, (i+1), option)# i+1
#                print("num_cluster为%s时" % (i+1))# i+1
                eva = evaluate(result, clu_list)
                if eva > best_eva:
                    best_eva = eva
                    best_k = i + 1
                    best_option = option
        print("选择mode为5(AgglomerativeClustering)时，linkage为%s" % best_option)
        print("采用NMI评测方法，best_k为%s时正确率最高，为%s" % (best_k, best_eva))
    elif mode == 6:
        result = dbscan(tfidf_matrix)
        best_eva = evaluate(result, clu_list)
        print("选择mode为6(DBSCAN)时，采用NMI评测方法，正确率为%s" % best_eva)
    elif mode == 7:
        result = birch(tfidf_matrix)
        best_eva = evaluate(result, clu_list)
        print("选择mode为7(Birch)时，采用NMI评测方法，best_k为90时正确率最高，为%s" % best_eva)


if __name__ == "__main__":
    DatasetPath = "D:\\projects\\python\\repository\\201814852ZhouPeiyan\\Homework3\\DataSet\\Tweets.txt"
    text_list, clu_list = preProcess(DatasetPath)
    print("共有%s条数据" % len(text_list))
    print("其中已知分类有%s种" % len(Counter(clu_list)))
    
    tfidf_matrix = tfidf(text_list)
    count_matrix = count(text_list)
    
    # 八种模型，1-K-means，2-AffinityPropagation，3-MeanShift，
    # 4-SpectralClustering，5-AgglomerativeClustering，6-DBSCAN，7-Birch
    for mode in range(1, 8):
        clustering(mode, tfidf_matrix, count_matrix, clu_list)
