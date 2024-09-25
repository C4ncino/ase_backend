import numpy as np
from dtaidistance import dtw

# Datos del acelerómetro: secuencias de coordenadas x, y, z
secuencias_acelerometro = [
    np.array([[0.1, 0.2, 0.1], [0.3, 0.4, 0.3], [0.5, 0.6, 0.5], [0.7, 0.8, 0.7], [0.9, 1.0, 0.9]]),
    np.array([[0.2, 0.3, 0.2], [0.4, 0.5, 0.4], [0.6, 0.7, 0.6], [0.8, 0.9, 0.8], [1.0, 1.1, 1.0]]),
    np.array([[1.5, 1.6, 1.5], [1.7, 1.8, 1.7], [1.9, 2.0, 1.9], [2.1, 2.2, 2.1], [2.3, 2.4, 2.3]]),
    np.array([[0.1, 0.1, 0.1], [0.2, 0.2, 0.2], [0.3, 0.3, 0.3], [0.4, 0.4, 0.4], [0.5, 0.5, 0.5]])
]

# Inicializar las matrices de distancias
distancias_x = np.zeros((len(secuencias_acelerometro), len(secuencias_acelerometro)))
distancias_y = np.zeros((len(secuencias_acelerometro), len(secuencias_acelerometro)))
distancias_z = np.zeros((len(secuencias_acelerometro), len(secuencias_acelerometro)))

# Calcular la distancia DTW entre secuencias para cada coordenada

for i in range(len(secuencias_acelerometro)):
    # Extraer columnas
    x_i = secuencias_acelerometro[i][:, 0]
    y_i = secuencias_acelerometro[i][:, 1]
    z_i = secuencias_acelerometro[i][:, 2]
    
    for j in range(len(secuencias_acelerometro)):
        if i != j:
            x_j = secuencias_acelerometro[j][:, 0]
            y_j = secuencias_acelerometro[j][:, 1]
            z_j = secuencias_acelerometro[j][:, 2]
            
            # Calcular distancias DTW para cada coordenada
            distancias_x[i, j] = dtw.distance(x_i, x_j)
            distancias_y[i, j] = dtw.distance(y_i, y_j)
            distancias_z[i, j] = dtw.distance(z_i, z_j)

# Calcular distancias promedio para cada coordenada
distancias_promedio_x = np.mean(distancias_x, axis=1)
distancias_promedio_y = np.mean(distancias_y, axis=1)
distancias_promedio_z = np.mean(distancias_z, axis=1)

# Imprimir las distancias promedio para cada coordenada
print (distancias_x)


print("Distancias promedio para coordenada x:")
for i, d_prom in enumerate(distancias_promedio_x):
    print(f"Distancia promedio de Secuencia {i+1}: {d_prom}")

print (distancias_y)


print("\nDistancias promedio para coordenada y:")
for i, d_prom in enumerate(distancias_promedio_y):
    print(f"Distancia promedio de Secuencia {i+1}: {d_prom}")

print (distancias_z)


print("\nDistancias promedio para coordenada z:")
for i, d_prom in enumerate(distancias_promedio_z):
    print(f"Distancia promedio de Secuencia {i+1}: {d_prom}")

# Definir un umbral de anomalía (media + desviación estándar) para cada coordenada
umbral_anomalia_x = np.mean(distancias_promedio_x) + np.std(distancias_promedio_x)
umbral_anomalia_y = np.mean(distancias_promedio_y) + np.std(distancias_promedio_y)
umbral_anomalia_z = np.mean(distancias_promedio_z) + np.std(distancias_promedio_z)

# Identificar las secuencias que superan el umbral de anomalía para cada coordenada
anomalías_x = np.where(distancias_promedio_x > umbral_anomalia_x)[0]
anomalías_y = np.where(distancias_promedio_y > umbral_anomalia_y)[0]
anomalías_z = np.where(distancias_promedio_z > umbral_anomalia_z)[0]

# Imprimir las secuencias que podrían ser anomalías para cada coordenada
print("\nSecuencias que podrían ser anomalías para coordenada x:")
for a in anomalías_x:
    print(f"Secuencia {a + 1} con distancia promedio: {distancias_promedio_x[a]}")

print("\nSecuencias que podrían ser anomalías para coordenada y:")
for a in anomalías_y:
    print(f"Secuencia {a + 1} con distancia promedio: {distancias_promedio_y[a]}")

print("\nSecuencias que podrían ser anomalías para coordenada z:")
for a in anomalías_z:
    print(f"Secuencia {a + 1} con distancia promedio: {distancias_promedio_z[a]}")
