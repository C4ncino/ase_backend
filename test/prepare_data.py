import os
import json
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

MAX_LEN = 60
WORDS = [
    'adios', 'alacran', 'animales', 'ayer', 'bien', 'como', 'como estas',
    'dia', 'feliz', 'gato', 'gracias', 'gustar', 'hola', 'medusa', 'mi',
    'nombre', 'perro', 'por favor', 'si', 'tacos'
]


def generate_random(quantity=20) -> np.ndarray:
    samples = []
    for _ in range(quantity):
        random_size = np.random.randint(54, 65)
        first_five = np.random.randint(0, 6, size=(random_size, 5))
        last_three = np.random.uniform(-9.99, 10.0, size=(random_size, 3))
        last_three = np.round(last_three, 2)
        samples.append(np.concatenate((first_five, last_three), axis=1))
    return np.array(samples, dtype=object)


def pad_sequences(in_array: list[np.ndarray], n=MAX_LEN):
    pad_sequence = []

    for sample in in_array:
        current_len = len(sample)

        if current_len < n:
            relleno = np.full((n - current_len, 8), 0.0)
            pad_sample = np.concatenate((sample, relleno))

        elif current_len > n:
            pad_sample = sample[:n]

        else:
            pad_sample = sample

        pad_sequence.append(pad_sample)

    return np.array(pad_sequence)


def generate_more_data(sensors_data: list[dict], new_samples=40):
    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
    sensors_dfs = [pd.DataFrame(sample) for sample in sensors_data]

    means_dfs = []

    for i in range(60):
        rows = []

        for df in sensors_dfs:
            try:
                rows.append(df.iloc[[i]])
            except IndexError:
                pass

        new_df = pd.concat(rows, ignore_index=True)
        means_dfs.append((new_df.mean(), new_df.std()))

    new_data = []

    for i in range(new_samples):
        random_len = random.randint(54, 60)

        new_data.append([])

        for j in range(random_len):
            means, stds = means_dfs[j]

            random_row = pd.Series({
                column: np.random.normal(loc=means[column], scale=stds[column] / 2)
                for column in means.index
            })

            for finger in fingers:
                random_row[finger] = round(random_row[finger])

            new_data[i].append(random_row.to_dict())

    for i in range(len(new_data)):
        df = pd.DataFrame(new_data[i])

        for column in ['x', 'y', 'z']:
            prev_val = df[column]

            df[column] = df[column].rolling(4).mean()
            df[column] = df[column].fillna(prev_val.iloc[0])
            df[column] = round(df[column], 2)

        new_data[i] = df.to_dict(orient='records')

    return new_data


def load_and_prepare_data_lg() -> tuple[np.ndarray, np.ndarray]:
    labels = []
    data = []

    i = 1

    for folder_path in WORDS:
        folder_path = os.path.join('data', folder_path)

        json_files = [
            f for f in os.listdir(folder_path)
            if f.endswith('.json')
        ]

        word_data = []

        for json_file in json_files:
            json_file_path = os.path.join(
                folder_path,
                json_file
            )

            with open(json_file_path) as f:
                json_data = json.load(f)
                word_data.append(json_data)

            labels.append(i)

        more = generate_more_data(word_data)

        word_data = word_data + more

        df_word_data = [
            pd.DataFrame(sample) for sample in word_data]

        data = data + df_word_data

        labels = labels + [i] * len(more)

        i += 1

    random_data = generate_random()
    data.extend(random_data)
    labels.extend([0] * len(random_data))

    data = pad_sequences(np.array(data, dtype=object))
    labels = np.array(labels)

    x_train, x_val, y_train, y_val = train_test_split(
        data, labels, test_size=0.2, stratify=labels
    )

    return x_train, x_val, y_train, y_val


def load_and_prepare_data(directory: str) -> tuple[np.ndarray, np.ndarray]:
    directory = os.path.join('data', directory)

    file_paths = [
        os.path.join(directory, f)
        for f in os.listdir(directory) if f.endswith('.json')
    ]

    data = []
    labels = []

    word_data = []

    for file_path in file_paths:
        with open(file_path) as f:
            json_data = json.load(f)

            word_data.append(json_data)

        labels.append(1)

    more = generate_more_data(word_data)
    word_data = word_data + more

    labels = labels + [1] * len(more)

    data = [pd.DataFrame(sample) for sample in word_data]

    if not data:
        raise ValueError("No se encontraron datos en los archivos JSON.")

    not_word = [elem for elem in WORDS if elem != directory]

    for folder_path in not_word:
        folder_path = os.path.join('data', folder_path)

        json_files = [
            f for f in os.listdir(folder_path)
            if f.endswith('.json')
        ]

        for json_file in json_files[:5]:
            json_file_path = os.path.join(
                folder_path,
                json_file
            )

            df = pd.read_json(json_file_path)

            data.append(df.values)
            labels.append(0)

    random_data = generate_random()
    data.extend(random_data)
    labels.extend([0] * len(random_data))

    data = pad_sequences(np.array(data, dtype=object))
    labels = np.array(labels)

    x_train, x_val, y_train, y_val = train_test_split(
        data, labels, test_size=0.2, stratify=labels
    )

    return x_train, x_val, y_train, y_val
