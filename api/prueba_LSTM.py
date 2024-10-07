import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import pandas as pd
import json
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score



# Datos 
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

n_samples = len(data)

# Dividir los datos en 80% entrenamiento y 20% validación usando Numpy
train_size = int(0.8 * n_samples)
indices = np.random.permutation(n_samples)
print(indices)

train_indices, val_indices = indices[:train_size], indices[train_size:]

X_train, X_val = data[train_indices], data[val_indices]
y_train, y_val = labels[train_indices], labels[val_indices]


print(y_train)
print(y_val)


# Definir el modelo LSTM
# model = Sequential()
# model.add(LSTM(256, input_shape=(timesteps, features), return_sequences=True)) #36
# model.add(Dropout(0.2))                                                      #0.1
# model.add(LSTM(128, return_sequences=True))                                                           #16 
# model.add(Dropout(0.3))    
# model.add(LSTM(64))   
# model.add(Dropout(0.3))   
# model.add(Dense(128, activation= 'relu'))   
# model.add(Dropout(0.4))                                                    #0.4
# model.add(Dense(3, activation='softmax')) 
                                  #1
                                #   
#Definir el modelo LSTM
model = Sequential()
model.add(LSTM(38, input_shape=(timesteps, features), return_sequences=True)) 
model.add(Dropout(0.1))                                                      
model.add(LSTM(16))                                                           
model.add(Dropout(0.2))   
model.add(Dense(10, activation= 'relu'))   
model.add(Dropout(0.4))                                                    
model.add(Dense(1, activation='sigmoid')) 

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=20, batch_size=8, validation_data=(X_val, y_val))


# ----------------------------------------------------------------------------------------

file_data = []

with open(r'C:\VScode\ase_backend\test\data\test.json') as f:
    json_data = json.load(f)

    for i in json_data:
        file_data.append(pd.DataFrame(i).values)

test_data = np.array(file_data)

print(len(test_data))

# test_labels = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0])
test_labels = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# Predecir en el conjunto de prueba
y_pred_proba = model.predict(test_data)

# Convertir probabilidades en clases (0, 1, o 2)
#y_pred = np.argmax(y_pred_proba, axis=1)

y_pred = (y_pred_proba >= 0.5).astype(int)

#print("Probabilidades predichas:\n", y_pred_proba)
#print("Clases predichas:\n", y_pred)

# Obtener métricas con scikit-learn
print("Accuracy:", accuracy_score(test_labels, y_pred))
print("Precision (macro):", precision_score(test_labels, y_pred, average='macro'))  # Promedio macro para clases múltiples
print("Recall (macro):", recall_score(test_labels, y_pred, average='macro'))
print("F1-Score (macro):", f1_score(test_labels, y_pred, average='macro'))

# Mostrar el reporte de clasificación completo para las 3 clases
print("\nClassification Report:\n", classification_report(test_labels, y_pred))

# Mostrar la matriz de confusión
print("\nConfusion Matrix:\n", confusion_matrix(test_labels, y_pred))