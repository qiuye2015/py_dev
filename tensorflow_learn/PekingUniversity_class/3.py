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
"""
六步法:
1. import
2. train, test
3. model = tf.keras.models.Sequential | class MyModel(Model) model=MyModel 
4. model.compile
5. model.fit
6. model.summary

拉直层：Flatten
全连接层：Dense
卷积层：Conv2D
LSTM层：LSTM
"""

# 导入数据,分别为输入特征和标签
x_train = datasets.load_iris().data
y_train = datasets.load_iris().target

# 随机打乱数据
np.random.seed(116)  # 使用相同的seed, 保证输入特征和标签一一对应
np.random.shuffle(x_train)

np.random.seed(116)
np.random.shuffle(y_train)
tf.random.set_seed(116)


# method 1
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(3, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2())
# ])
# method 2
class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        # 定义网络结构块
        self.d1 = tf.keras.layers.Dense(3, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l2())

    def call(self, x):
        # 调用网络结构块，实现前向传播
        y = self.d1(x)
        return y


model = MyModel()

model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.1),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),  # 由于softmax, 所以设置Flase 使得y符合概率分布
              metrics=['sparse_categorical_accuracy'])  # y_ 是数值, 预测y是独热码(概率分布)

# validation_freq 多少个epoch测试一次
model.fit(x_train, y_train, batch_size=32, epochs=500, validation_split=0.2, validation_freq=20)

model.summary()
