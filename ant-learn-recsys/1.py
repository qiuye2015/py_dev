import numpy as np
import pandas as pd
import matplotlib as mpl
import sklearn
import tensorflow as tf
import flask

for module in (np, pd, mpl, sklearn, tf, flask):
    print(f"{module.__name__}\t{module.__version__}")
