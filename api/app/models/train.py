import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from app.database import database


def prepare_data(sensor_data: list[dict], user_id: int):
    n_samples = len(sensor_data)

    current_data = np.array([pd.DataFrame(i).values for i in sensor_data])
    current_labels = np.array([1]*n_samples)

    user_words = database.read_by_field('words', 'user_id', user_id)

    other_words_data = []

    for word in user_words:
        word_data = database.read_by_id('data_words', word.id)

        json = word_data.data

        for i in range(5):
            other_words_data.append(pd.DataFrame(json[i]).values)

    data = np.concatenate((current_data, np.array(other_words_data)))

    labels = np.concatenate((current_labels, np.zeros(len(other_words_data))))

    x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2)

    return x_train, x_val, y_train, y_val
