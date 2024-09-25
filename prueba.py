import numpy as np
from dtaidistance import dtw

# Datos del acelerómetro: secuencias de coordenadas x, y, z
secuencias_acelerometro = [
    np.array([[0.1, 0.2, 0.1], [0.3, 0.4, 0.3], [0.5, 0.6, 0.5], [0.7, 0.8, 0.7], [0.9, 1.0, 0.9]]),
    np.array([[0.2, 0.3, 0.2], [0.4, 0.5, 0.4], [0.6, 0.7, 0.6], [0.8, 0.9, 0.8], [1.0, 1.1, 1.0]]),
    np.array([[1.5, 1.6, 1.5], [1.7, 1.8, 1.7], [1.9, 2.0, 1.9], [2.1, 2.2, 2.1], [2.3, 2.4, 2.3]]),
    np.array([[0.1, 0.1, 0.1], [0.2, 0.2, 0.2], [0.3, 0.3, 0.3], [0.4, 0.4, 0.4], [0.5, 0.5, 0.5]])
]

# Calcular la distancia DTW entre dos secuencias

distancias = np.zeros((len(secuencias_acelerometro), len(secuencias_acelerometro)))

for i in range(len(secuencias_acelerometro)):
    for j in range(len(secuencias_acelerometro)):
        if i != j:
            distancias[i, j] = dtw.distance(secuencias_acelerometro[i].flatten(), secuencias_acelerometro[j].flatten())

print("Matriz de distancias DTW:")
print(distancias)

# -----------------------deteccion de anomalias----------------------

distancias_promedio = np.mean(distancias, axis=1)

# Imprimir las distancias promedio

for i, d_prom in enumerate(distancias_promedio):
    print(f"Distancia promedio de Secuencia {i+1}: {d_prom}")

# Definir un umbral de anomalía (media + desviación estándar)
umbral_anomalia = np.mean(distancias_promedio) + np.std(distancias_promedio)

# Identificar las secuencias que superan el umbral de anomalía
anomalías = np.where(distancias_promedio > umbral_anomalia)[0]

print("\nSecuencias que podrían ser anomalías:")
for a in anomalías:
    print(f"Secuencia {a + 1} con distancia promedio: {distancias_promedio[a]}")
