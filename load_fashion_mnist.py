# -*- coding: utf-8 -*-
"""Load fashion MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eeid6JaP0zjh0dhFjBz6KwLkUz-41STG
"""

import tensorflow as tf
import numpy as np

tf.keras.backend.clear_session()
tf.random.set_seed(51)
np.random.seed(51)

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
 
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

train_gen = tf.keras.preprocessing.image.ImageDataGenerator(
    horizontal_flip=True,
    vertical_flip=True,
    width_shift_range=0.05,
    height_shift_range=0.05,
    shear_range=0.05,
)
train_dataset = tf.keras.preprocessing.image.NumpyArrayIterator(image_data_generator=train_gen,
                                                                x=x_train, y=y_train,
                                                                shuffle=True, seed=1024, )

test_gen = tf.keras.preprocessing.image.ImageDataGenerator()
test_dataset = tf.keras.preprocessing.image.NumpyArrayIterator(image_data_generator=test_gen,
                                                               x=x_test, y=y_test, )

#  List 1 batch
# for item in train_dataset.take(1):
#    print(item)

model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(filters=256, 
                         kernel_size=2, 
                         input_shape=(28, 28, 1),
                         activation=tf.keras.activations.relu), 
  tf.keras.layers.MaxPooling2D(pool_size=2, padding="valid"),     

  tf.keras.layers.Dropout(.2),

  tf.keras.layers.Conv2D(filters=128, 
                         kernel_size=2, 
                         activation=tf.keras.activations.relu), 
  tf.keras.layers.MaxPooling2D(pool_size=2, padding="valid"),  
  
  tf.keras.layers.Dropout(.1),

  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(10, activation=tf.keras.activations.softmax)
])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=["accuracy"])
model.summary()

history = model.fit(train_dataset,
                    batch_size=32,
                    epochs=100,
                    validation_data=test_dataset, )

import matplotlib.pyplot as plt

def plot(history, m, label, title):
  print([k for k in history.history])
  v = history.history[m]
  val_v = history.history[f"val_{m}"]

  epochs = range(1, len(v) + 1)

  plt.plot(epochs, v, 'b', label=label)
  plt.plot(epochs, val_v, 'r', label=f"val_{label}")

  plt.title(title)

  plt.xlabel('Epochs')
  plt.ylabel(label)

  plt.legend()
  plt.show()

plot(history, "accuracy", "accuracy", "Train & Validation accuracy")

plot(history, "loss", "loss", "Train & Validation loss")