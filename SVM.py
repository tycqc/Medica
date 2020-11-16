import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

'''数据集载入与数据分割'''
# 加载二分类乳腺癌数据集
cancer = load_breast_cancer()
# 打印数据集信息
print("数据集样本数：", cancer.data.shape[0])
print("每个样本特征数：", cancer.data.shape[1])
print("样本类别：", np.unique(cancer.target))
# 划分数据集
X = cancer.data  # 获取数据集的特征
y = cancer.target  # 获取数据集的类别
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # 将数据集划分为训练集与测试集
'''模型训练与预测'''
clf = SVC(C=1.0, kernel='linear')  # 初始化SVM模型，C为正则化系数（C越大则对训练集效果越好，可能导致泛化性能变差），kernel为核函数
clf.fit(X_train, y_train)  # 训练SVM模型
predict = clf.predict(X_test)  # 得到预测的标签值
print('测试集的预测准确率为：{}%'.format(clf.score(X_test, y_test) * 100))  # 获取模型对测试集的预测准确率
'''绘图'''
wrong_point = []  # 误分类点集合
health = []  # 类别0（乳腺癌阴性）集合
sick = []  # 类别1（乳腺癌阳性）集合
for i in range(len(X_test)):
    if y_test[i] != predict[i]:
        wrong_point.append([X_test[i][0], X_test[i][1]])
    else:
        if y_test[i] == 0:
            health.append([X_test[i][0], X_test[i][1]])
        else:
            sick.append([X_test[i][0], X_test[i][1]])
plt.scatter([x[0] for x in wrong_point], [x[1] for x in wrong_point], c='red', label='误分类点')  # 误分类点标记为红色
plt.scatter([x[0] for x in health], [x[1] for x in health], c='black', label='阴性')  # 类别为0(乳腺癌阴性)则标记为黑色
plt.scatter([x[0] for x in sick], [x[1] for x in sick], c='green', label='阳性')  # 类别为1(乳腺癌阳性)则标记为绿色
plt.title('基于SVM的乳腺癌分类诊断')  # 设置图片标题
plt.legend()  # 设置图片标签
plt.show()