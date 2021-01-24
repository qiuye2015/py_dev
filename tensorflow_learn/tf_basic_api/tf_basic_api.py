import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import pandas as pd
import os
import sys
import time
import tensorflow as tf

from tensorflow import keras

print(tf.__version__)
print(sys.version_info)
for module in mpl, np, pd, sklearn, tf, keras:
    print(module.__name__, module.__version__)
print("*" * 66)

# index
t = tf.constant([[1, 2, 3], [4, 5, 6]])
print(t)
print(t[:, 1:])
print(t[..., 1])

# op
