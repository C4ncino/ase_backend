import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from app.database import database

MAX_LEN = 60


def generate_random(quantity=20) -> np.ndarray:
    samples = []

    for _ in range(quantity):
        random_size = np.random.randint(54, 65)

        first_five = np.random.randint(0, 6, size=(60, 5))

        first_five = np.random.randint(0, 6, size=(random_size, 5))

        last_three = np.random.uniform(-9.99, 10.0, size=(random_size, 3))

        last_three = np.round(last_three, 2)

        samples.append(np.concatenate((first_five, last_three), axis=1))

    samples_array = np.array(samples, dtype=object)

    return samples_array


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


def prepare_data(sensor_data: list[dict], user_id: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    n_samples = len(sensor_data)

    current_data = np.array([pd.DataFrame(i).values for i in sensor_data], dtype=object)
    current_labels = np.array([1]*n_samples)

    user_words = database.read_by_field('words', 'user_id', user_id)

    other_words_data = []

    for word in user_words:
        word_data = database.read_by_id('data_words', word.id)

        json = word_data.data

        for i in range(5):
            other_words_data.append(pd.DataFrame(json[i]).values)

    if len(other_words_data) > 0:
        labels = np.concatenate(
            (current_labels, np.zeros(len(other_words_data)), np.zeros(20))
        )

        other_words_data = np.array(other_words_data, dtype=object)

        data = np.concatenate(
            (current_data, other_words_data, generate_random())
        )

    else:
        data = np.concatenate((current_data, generate_random()))
        labels = np.concatenate((current_labels, np.zeros(20)))

    data = pad_sequences(data)

    x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, stratify=labels)

    return x_train, x_val, y_train, y_val


def prepare_data_for_lm(user_id: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    user_words = database.read_by_field('words', 'user_id', user_id)

    training_data_arr = []
    labels_arr = []

    for word in user_words:
        word_data = database.read_by_id('data_words', word.id)

        json = word_data.data

        for sample in json:
            training_data_arr.append(pd.DataFrame(sample).values)
            labels_arr.append(word.class_key)

    training_data = np.array(training_data_arr, dtype=object)

    data = np.concatenate((training_data, generate_random()))
    labels = np.concatenate((np.array(labels_arr), np.zeros(20)))

    data = pad_sequences(data)

    x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, stratify=labels)

    return x_train, x_val, y_train, y_val, len(user_words) + 1
