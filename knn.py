import numpy as np
import operator


def autonorm(data):#归1化
    mn = data.min(0)
    mx = data.max(0)
    range = mx - mn
    normdata = np.zeros(np.shape(data))
    normdata = (data - mn) / range
    return normdata

def knn(mat,test, k,flag):#flag等于1，训练找最佳k，flag = 0测试，mat为训练集，test为测试集
    corr = 0
    trainsize = len(mat)
    testsize = len(test)

    del label[:]#用来记录测试时的答案
    for i in range(testsize):
        diff = np.tile(test[i], (trainsize,1)) - mat
        squr = diff ** 2# 每个维度的欧式距离
        distance = (squr.sum(axis=1))**0.5
        sortdistance = distance.argsort()
        classcount = {}#字典来计数
        for j in range(1,k+1):#记录统计最近k个邻居的种类,最近的是本身
            votelabel = str(alabel[sortdistance[j]][0])#记录最近点的label
            classcount[votelabel] = classcount.get(votelabel,0) + 1 #此时每个点在统计种类是都是1，根据距离越近越相似的观点，此处可以对近的点加一个大的权重
        sortedclasscount = sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
        if flag == 1:
            if sortedclasscount[0][0] == alabel[i]:
                corr += 1
        else:
            label.append(sortedclasscount[0][0])

    if flag == 1:
        print(corr /trainsize)
        acc.append(corr / trainsize)


if '__main__' == __name__:
    label = []#记录最后预测结果
    acc = []#记录训练K时，不同k对应的正确率

    train_filename = r"./train.txt"
    test_filename = r"./test.txt"
    an_filename = r"./ans.txt"
    datas = np.loadtxt(train_filename, delimiter=",", dtype=str)
    data = datas[:, 0:4]
    data = data.astype(np.float)
    tlabel = []
    c = datas[:, 4:5]
    for i in range(len(c)):
        tlabel.append(c[i])
    datatrain = data
    alabel = tlabel


    trainData = autonorm(datatrain)
    for i in range(1,11):
        print("k == %d" %i)
        knn(trainData,trainData,i,1)
    print("发现k=%d 时，正确率最高" %(acc.index(max(acc))+1) )

    data2 = np.loadtxt(test_filename, delimiter=",", dtype=str)
    datatest = data2[:, 0:4]
    datatest = datatest.astype(np.float)


    test = autonorm(datatest)
    le = len(test)

    knn(trainData,test,(acc.index(max(acc))+1),0)

    fl=open(an_filename, 'w')
    for i in label:
        fl.write(i)
        fl.write("\n")
    fl.close()
