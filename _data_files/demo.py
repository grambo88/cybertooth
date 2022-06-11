import tensorflow as tf
import pandas as pd 
import numpy as np

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.utils import shuffle
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

data = pd.read_csv('horse_stats.csv')
data = shuffle(data, random_state=22)

print(data.head())
print('\n')
print(data)
print(data.tail())
