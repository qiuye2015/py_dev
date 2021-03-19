import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import sys
import time
import tensorflow as tf
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
print("*" * 66)
print(tf.__version__)
print("*" * 66)

# tf.Variable 将变量标记为可训练的
w = tf.Variable(tf.constant(5, dtype=tf.float32))
lr = 0.2
epochs = 40

for epoch in range(epochs):
    with tf.GradientTape() as tape:
        loss = tf.square(w + 1)

    grads = tape.gradient(loss, w)  # .gradient函数告知对谁求导

    print("After %s epoch, loss is %f, w is %f " % (epoch, loss, w.numpy()))
    w.assign_sub(lr * grads)  # w -= lr * grads

"""
epoch   w                       loss
0       5                        36  
1       5-0.2*[2*(w+1)]=2.6      12.96 
"""
