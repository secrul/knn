import numpy as np
import operator


label = []#记录最后预测结果
list = []#记录训练K时，不同k对应的正确率
vec_num = int(input("输入向量的维度(不包括标签)："))

train_filename = r"D:\train.txt"
test_filename = r"D:\test.txt"
an_filename = r"D:\an.txt"

def filetodata(flag):
    a = np.loadtxt(train_filename, delimiter=",", dtype=str)
    b = a[:, 0:4]
    b = b.astype(np.float)
    d = []
    if flag == 0:
        return b
    else:
        c = a[:, 4:4+1]
        for i in range(len(c)):
            d.append(c[i][0])
        return b, d

def autonorm(data):#归1化
    mn = data.min(0)
    mx = data.max(0)
    range = mx - mn
    normdata = np.zeros(np.shape(data))
    normdata = (data - mn) / range
    return normdata

def knn(mat,test, k,flag):#训练找最佳k时flag等于1，测试时flag = 0，mat为训练集，test为测试集
    corr = 0
    trainsize = len(mat)
    testsize = len(test)

    del label[:]#用来记录测试时的答案
    for i in range(testsize):
        diff = np.tile(test[i], (trainsize,1)) - mat
        squr = diff ** 2
        distance = (squr.sum(axis=1))**0.5
        sortdistance = distance.argsort()
        classcount = {}#字典来计数
        for j in range(flag,k+flag):#当训练k的值时，flag = 1；从最近的第二个开始计数，因为第一个是其本身，为0
            votelabel = alabel[sortdistance[j]]#记录最近点的label
            classcount[votelabel] = classcount.get(votelabel,0) + 1
        sortedclasscount = sorted(classcount.items(),key=operator.itemgetter(1),reverse=True)
        if flag == 1:
            if sortedclasscount[0][0] == alabel[i]:
                corr += 1
        else:
            label.append(sortedclasscount[0][0])
    if flag == 1:
        print(corr /trainsize)
        list.append(corr / trainsize)

a = np.loadtxt(train_filename, delimiter=",", dtype=str)
b = a[:, 0:vec_num]
b = b.astype(np.float)
d = []
c = a[:, vec_num:vec_num+1]
for i in range(len(c)):
    d.append(c[i][0])
datatrain = b
alabel = d

onemat = autonorm(datatrain)
for i in range(1,11):
    print("k == %d" %i)
    knn(onemat,onemat,i,1)
print("发现k=%d 时，正确率最高" %(list.index(max(list))+1) )

c = np.loadtxt(test_filename, delimiter=",", dtype=str)
datatest = c[:, 0:4]
datatest = datatest.astype(np.float)



print(datatest)
onemat1 = autonorm(datatest)
le = len(onemat1)

knn(onemat,onemat1,(list.index(max(list))+1),0)

fl=open(an_filename, 'w')
for i in label:
    fl.write(i)
    fl.write("\n")
fl.close()

print(len(label))
