import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import sys
import time
import tensorflow as tf
from sklearn import datasets
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
print("*" * 66)
print(tf.__version__)
print("*" * 66)

# 导入数据,分别为输入特征和标签
x_data = datasets.load_iris().data
y_data = datasets.load_iris().target

# 随机打乱数据
np.random.seed(116)  # 使用相同的seed, 保证输入特征和标签一一对应
np.random.shuffle(x_data)

np.random.seed(116)
np.random.shuffle(y_data)
tf.random.set_seed(116)

# 分割为测试集和训练集
x_train = x_data[:-30]
y_train = y_data[:-30]
x_test = x_data[-30:]
y_test = y_data[-30:]

x_train = tf.cast(x_train, tf.float32)
x_test = tf.cast(x_test, tf.float32)

# 使输入特征和标签值一一对应
train_db = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(32)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

# 生成神经网络参数,4个输入特征,3个分类
# tf.Variable 标记参数可训练
w1 = tf.Variable(tf.random.truncated_normal([4, 3], stddev=0.1, seed=1))
b1 = tf.Variable(tf.random.truncated_normal([3], stddev=0.1, seed=1))

train_loss_results = []
test_acc = []
lr = 0.1
epoch = 500
loss_all = 0

for epoch in range(epoch):  # 数据集级别的循环，每个epoch循环一次数据集
    for step, (x_train, y_train) in enumerate(train_db):  # batch级别的循环
        with tf.GradientTape() as tape:  # with结构几轮梯度信息
            y = tf.matmul(x_train, w1) + b1
            y = tf.nn.softmax(y)  # 使输入y符合概率分布

            y_ = tf.one_hot(y_train, depth=3)
            loss = tf.reduce_mean(tf.square(y_ - y))  # 采用均方误差损失函数
            loss_all += loss.numpy()

        grads = tape.gradient(loss, [w1, b1])  # 计算loss对各个参数的梯度

        # 实现梯度更新 w1 = w1 - lr * w1_grad  b1 = b1 - lr * b1_grad
        w1.assign_sub(lr * grads[0])
        b1.assign_sub(lr * grads[1])
    # 每个epoch 打印loss信息
    print("Epoch:{}, loss:{}".format(epoch, loss_all / 4))
    train_loss_results.append(loss_all / 4)
    loss_all = 0

    # total_correct为预测对样本个数, total_number 为测试样本总数
    total_correct, total_number = 0, 0
    for x_test, y_test in test_db:
        y = tf.matmul(x_test, w1) + b1
        y = tf.nn.softmax(y)
        pred = tf.argmax(y, axis=1)  # 返回y中最大值的索引
        pred = tf.cast(pred, dtype=y_test.dtype)

        # 若分类正确,则correct=1,否则为0
        correct = tf.cast(tf.equal(pred, y_test), dtype=tf.int32)
        # 将每个batch的correct数加起来
        correct = tf.reduce_sum(correct)

        total_correct += int(correct)
        total_number += x_test.shape[0]

    acc = total_correct / total_number
    test_acc.append(acc)
    print("Test_acc:", acc)
    print("-" * 30)

# 绘制loss曲线
plt.title("Loss Function Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.plot(train_loss_results, label="$Loss$")
plt.legend()  # 画出曲线图标
plt.show()  # 画出图像

# 绘制Accuracy曲线
plt.title("Acc Curve")
plt.xlabel("Epoch")
plt.ylabel("Acc")
plt.plot(test_acc, label="$Accuracy$")
plt.legend()  # 画出曲线图标
plt.show()  # 画出图像
