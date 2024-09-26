import numpy as np
# import tensorflow as tf
# import keras
# from keras import layers, models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pandas as pd
import json

# Datos 
n_samples = 19
timesteps = 60  # 60 mediciones por muestra
features = 8    # 8 características

labels = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

a = []

with open(r'C:\VScode\ase_backend\test\data\algo.json') as f:
    json_data = json.load(f)

    for i in json_data:
        a.append(pd.DataFrame(i).values)

data = np.array(a)

print(len(data))

# Dividir los datos en 80% entrenamiento y 20% validación usando Numpy
train_size = int(0.8 * n_samples)
indices = np.random.permutation(n_samples)
train_indices, val_indices = indices[:train_size], indices[train_size:]

X_train, X_val = data[train_indices], data[val_indices]
y_train, y_val = labels[train_indices], labels[val_indices]

# Definir el modelo LSTM
model = Sequential()
model.add(LSTM(32, input_shape=(timesteps, features), return_sequences=True))
model.add(LSTM(16))
model.add(Dense(1, activation='sigmoid'))

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=20, batch_size=10, validation_data=(X_val, y_val))
