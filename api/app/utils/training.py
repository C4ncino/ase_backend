import numpy as np
import pandas as pd
from dtaidistance import dtw
from sklearn.neighbors import NearestNeighbors


def inspect_fingers(sensor_data):
    df_fingers = [
        pd.DataFrame(mov).loc[:, ['thumb', 'index', 'middle', 'ring', 'pinky']]
        for mov in sensor_data
    ]

    df_means = pd.DataFrame([df.mean().to_dict() for df in df_fingers])

    centroid = df_means.mean().values.reshape(1, -1)

    distances = np.linalg.norm(df_means - centroid, axis=1)

    radius = np.mean(distances) + 2 * np.std(distances)

    knn = NearestNeighbors(radius=radius)

    knn.fit(df_means)

    _, indices = knn.radius_neighbors(centroid)

    neighbors_within_radius: pd.DataFrame = df_means.iloc[indices[0]]

    centroid = neighbors_within_radius.mean().values.reshape(1, -1)

    return indices[0], centroid


def inspect_movement(sensor_data):
    dfs_accel = [
        pd.DataFrame(mov).loc[:, ['x', 'y', 'z']]
        for mov in sensor_data
    ]

    distances = np.zeros((len(dfs_accel), len(dfs_accel)))

    for i in range(len(dfs_accel)):
        for j in range(len(dfs_accel)):
            if i == j:
                continue

            distances[i, j] = dtw.distance(
                dfs_accel[i].values.flatten(),
                dfs_accel[j].values.flatten()
            )

    mean_distances = np.mean(distances, axis=1)

    threshold = np.mean(mean_distances) + 2 * np.std(mean_distances)

    bad_samples = np.where(mean_distances > threshold)[0]

    return bad_samples
