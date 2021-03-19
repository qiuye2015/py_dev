import sklearn  # 必须在import tensorflow 之前,要不出错
import tensorflow as tf

import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
print("*" * 66)
print(tf.__version__)
print("*" * 66)

model_save_path = "./checkpoint/mnist.ckpt"

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.load_weights(model_save_path)

preNum = int(input("input the number of test pic: "))

for i in range(preNum):
    image_path = input('the path of test pic: ')
    img = Image.open(image_path)
    img = img.resize((28, 28), Image.ANTIALIAS)
    img_arr = np.array(img.convert('L'))

    img_arr = 255 - img_arr
    img_arr = img_arr / 255.
    print("img_arr:", img_arr.shape)
    x_predict = img_arr[tf.newaxis, ...]
    print("x_predict", x_predict.shape)
    result = model.predict(x_predict)

    pred = tf.argmax(result, axis=1)
    tf.print(pred)
