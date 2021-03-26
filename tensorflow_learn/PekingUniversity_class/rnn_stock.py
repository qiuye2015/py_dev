import sklearn  # 必须在import tensorflow 之前,要不出错
import tensorflow as tf
from tensorflow.keras.layers import Dropout, Dense, SimpleRNN, LSTM, GRU

from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import pandas as pd

import os
import math

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
print("*" * 120)
print(tf.__version__)
print("*" * 120)

maotai = pd.read_csv('./SH600519.csv')

training_set = maotai.iloc[0:2426 - 300, 2:3].values  # 前2426-300天的开盘价作为训练集, 2:3是提取[2:3)列数据,故提取开盘价
test_set = maotai.iloc[2426 - 300:, 2:3].values  # 后300天的开盘价作为测试集

# 归一化
sc = MinMaxScaler(feature_range=(0, 1))  # 定义归一化：归一化到0-1之间
training_set_scaled = sc.fit_transform(training_set)  # 求得训练集的最大值，最小值，并在训练集上进行归一化
test_set_scaled = sc.transform(test_set)  # 利用训练集的属性对测试集进行归一化

x_train = []
y_train = []
x_test = []
y_test = []

# 利用for循环，遍历训练集，提取训练集中中连续60天的开盘价作为输入特征x_train,第61天的数据作为标签;共2426-300-60组数据
for i in range(60, len(training_set_scaled)):
    x_train.append(training_set_scaled[i - 60:i, 0])
    y_train.append(training_set_scaled[i, 0])

# 打乱训练集顺序
np.random.seed(7)
np.random.shuffle(x_train)
np.random.seed(7)
np.random.shuffle(y_train)
tf.random.set_seed(7)

# 将训练集由list格式变为array格式
x_train, y_train = np.array(x_train), np.array(y_train)
# 使x_train符合RNN输入要求：[送入样本数, 循环核时间展开步数,每个时间步输入特征数]
# 此处整个数据集送入,选入样本数为x_train.shape[0];输入60个开盘价,预测出第61天开盘价,循环核时间展开步为60;
# 每个时间步送入的特征是某一天的开盘价,只有1个数据,故每个时间步输入特征个数为1
x_train = np.reshape(x_train, (x_train.shape[0], 60, 1))

# 测试集
for i in range(60, len(test_set_scaled)):
    x_test.append(test_set_scaled[i - 60:i, 0])
    y_test.append(test_set_scaled[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
x_test = np.reshape(x_test, (x_test.shape[0], 60, 1))

# model = tf.keras.Sequential([
#     SimpleRNN(80, return_sequences=True),
#     Dropout(0.2),
#     SimpleRNN(100),
#     Dropout(0.2),
#     Dense(1)
# ])

# model = tf.keras.Sequential([
#     LSTM(80, return_sequences=True),
#     Dropout(0.2),
#     LSTM(100),
#     Dropout(0.2),
#     Dense(1)
# ])

model = tf.keras.Sequential([
    GRU(80, return_sequences=True),
    Dropout(0.2),
    GRU(100),
    Dropout(0.2),
    Dense(1)
])

model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss='mean_squared_error')
# 该应用只观测loss数值,不观测准确率,所以删去metirc选项

# checkpoint_save_path = './checkpoint/stock.ckpt'
checkpoint_save_path = './checkpoint/GRU_stock.ckpt'

if os.path.exists(checkpoint_save_path + ".index"):
    print('-------------load the model-----------------')
    model.load_weights(checkpoint_save_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                 save_weights_only=True,
                                                 save_best_only=True,
                                                 monitor='val_loss')

history = model.fit(x_train, y_train, batch_size=64, epochs=50,
                    validation_data=(x_test, y_test),
                    callbacks=[cp_callback])

model.summary()

# print(model.trainable_variables)
file = open('./weights.txt', 'w')
for v in model.trainable_variables:
    file.write(str(v.name) + '\n')
    file.write(str(v.shape) + '\n')
    file.write(str(v.numpy()) + '\n')
file.close()

###############################################    show   ##############################################################
# 显示训练集和验证集的acc和loss曲线

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()
###############################################    predict   ###########################################################
predicted_stock_price = model.predict(x_test)
# 对预测数据还原----从(0,1)反归一化到原始范围
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
# 对真实数据还原----从(0,1)反归一化到原始范围
real_stock_price = sc.inverse_transform(test_set_scaled[60:])
# 画出真实数据和预测数据的对比曲线
plt.plot(real_stock_price, color='red', label='MaoTai Stock Price')
plt.plot(predicted_stock_price, color='blue', label='Predict MaoTai Stock Price')
plt.title('MaoTai Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('MaoTai Stock Price')
plt.legend()
plt.show()

###############################################    evaluate   ##########################################################
mse = mean_squared_error(predicted_stock_price, real_stock_price)
rmse = math.sqrt(mse)
mae = mean_absolute_error(predicted_stock_price, real_stock_price)
print('均方误差：%.6f' % mse)
print('均方根误差：%.6f' % rmse)
print('平均绝对误差：%.6f' % mae)
