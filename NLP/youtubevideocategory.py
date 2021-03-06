# -*- coding: utf-8 -*-
"""YoutubeVideo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h8b37YNDQKLqa8_v7cy2YxhYWucLDao-
"""

!wget --no-check-certificate \
https://raw.githubusercontent.com/luthfi11/Learn-Machine-Learning/master/Youtube%20Video%20Dataset.csv -O /tmp/dataset.csv

import pandas as pd

dataset = pd.read_csv("/tmp/dataset.csv")
dataset

category = pd.get_dummies(dataset.Category)

new_data = pd.concat([dataset[['Title']], category], axis=1)
new_data

title = new_data['Title'].values
label = new_data.loc[:, new_data.columns != 'Title'].values

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(title, label, test_size=0.2)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=1000, oov_token='x')

tokenizer.fit_on_texts(X_train) 
tokenizer.fit_on_texts(X_test)
 
sequences_train = tokenizer.texts_to_sequences(X_train)
sequences_test = tokenizer.texts_to_sequences(X_test)
 
padded_train = pad_sequences(sequences_train) 
padded_test = pad_sequences(sequences_test)

import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=1000, output_dim=16),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

num_epochs = 30
history = model.fit(padded_train, y_train, epochs=num_epochs, 
                    validation_data=(padded_test, y_test), 
                    verbose=2)