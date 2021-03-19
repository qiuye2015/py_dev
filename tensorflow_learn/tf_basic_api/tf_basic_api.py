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

from tensorflow import keras

print(tf.__version__)
print(sys.version_info)
for module in mpl, np, pd, sklearn, tf, keras:
    print(module.__name__, module.__version__)
print("*" * 66)
# print()

# index
# t = tf.constant([[1, 2, 3], [4, 5, 6]])
# print(t)
# print(t[:, 1:])
# print(t[..., 1])

# op
x = tf.constant([[1.0, 2.0]])
w = tf.constant([[3.0], [4.0]])
y = tf.matmul(x, w)
print(y)

print("*" * 66)
