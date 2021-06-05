from tensorflow.keras import layers, models, Sequential, layers
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping

from numpy.random import seed
from tensorflow.random import set_seed
from tensorflow import random


def initialize_compile_model(input_shape=(100,100,3),categories=16):

  model = models.Sequential()
  
  model.add(Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape))
  model.add(MaxPooling2D((2, 2)))
  model.add(Dropout(0.2))

  model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
  model.add(MaxPooling2D((3, 3)))
  model.add(Dropout(0.2))

  model.add(Conv2D(128, (2, 2), activation='relu', padding='same'))
  model.add(MaxPooling2D((2, 2)))
  model.add(Dropout(0.3))
  
  model.add(Flatten())
  model.add(Dense(100, activation='relu'))
  model.add(Dropout(0.4))
  model.add(Dense(categories, activation='softmax'))

  model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
  return model