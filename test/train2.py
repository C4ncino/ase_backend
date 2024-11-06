import os
import numpy as np
import pandas as pd

from tensorflow import get_logger
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, f1_score, roc_auc_score
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score

from models import get_model, SMALL_MODELS

MAX_LEN = 60

WORDS = [
    'adios', 'alacran', 'animales', 'ayer', 'bien', 'como', 'como estas',
    'dia', 'feliz', 'gato', 'gracias', 'gustar', 'hola', 'medusa', 'mi',
    'nombre', 'perro', 'por favor', 'si', 'tacos'
]

get_logger().setLevel('ERROR')


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


def load_and_prepare_data(directory: str) -> tuple[np.ndarray, np.ndarray]:
    directory = os.path.join('data', directory)

    file_paths = [
        os.path.join(directory, f)
        for f in os.listdir(directory) if f.endswith('.json')
    ]

    data = []
    labels = []

    for file_path in file_paths:
        df = pd.read_json(file_path)
        data.append(df.values)
        labels.append(1)

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


def calc_metrics(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average='macro'),
        "recall": recall_score(y_true, y_pred, average='macro'),
        "f1_score": f1_score(y_true, y_pred, average='macro'),
        "roc_auc": roc_auc_score(y_true, y_pred),
        "confusion_matrix": confusion_matrix(y_true, y_pred)
    }


def pretty_print_metrics(data, current_word: str):

    file_name = f"results_{current_word}.txt"
    file_path = os.path.join('results/txts', file_name)

    with open(file_path, 'w') as file:
        for label, metrics_list in data.items():
            file.write(f"\n{'='*45}")
            file.write(f"\n           Results for {label}")

            avg_metrics = {
                "accuracy": 0,
                "precision": 0,
                "recall": 0,
                "f1_score": 0,
                "roc_auc": 0
            }

            num_entries = len(metrics_list)
            for metrics in metrics_list:
                avg_metrics["accuracy"] += metrics["accuracy"]
                avg_metrics["precision"] += metrics["precision"]
                avg_metrics["recall"] += metrics["recall"]
                avg_metrics["f1_score"] += metrics["f1_score"]
                avg_metrics["roc_auc"] += metrics["roc_auc"]

            for key in avg_metrics:
                avg_metrics[key] /= num_entries

            file.write(f"\n\n+ {'-'*33} +")
            file.write("\n|             Averages              |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")
            file.write(f"\n| {'Metric':<15} | {'Value':<15} |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")
            file.write(f"\n| {'Accuracy':<15} | {avg_metrics['accuracy']:.5f}         |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")
            file.write(f"\n| {'Precision':<15} | {avg_metrics['precision']:.5f}         |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")
            file.write(f"\n| {'Recall':<15} | {avg_metrics['recall']:.5f}         |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")
            file.write(f"\n| {'F1 Score':<15} | {avg_metrics['f1_score']:.5f}         |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")
            file.write(f"\n| {'ROC AUC':<15} | {avg_metrics['roc_auc']:.5f}         |")
            file.write(f"\n+ {'-'*15} + {'-'*15} +")

            file.write(f"\n\n+ {'-'*39} +")
            file.write("\n|                 Matrices                |")
            file.write(f"\n+ {'-'*39} +")
            file.write(f"\n{'+ --- +  '*5}\n")

            for _, metrics in enumerate(metrics_list, start=1):
                a = metrics['confusion_matrix'][0][0]
                b = metrics['confusion_matrix'][0][1]
                file.write(f"|{a:>2} {b:>2}|  ")

            file.write(f"\n{'+ --- +  '*5}\n")
            for _, metrics in enumerate(metrics_list, start=1):
                a = metrics['confusion_matrix'][1][0]
                b = metrics['confusion_matrix'][1][1]
                file.write(f"|{a:>2} {b:>2}|  ")

            file.write(f"\n{'+ --- +  '*5}")

            file.write(f"\n\n{'='*45}\n")


def train(directory):

    train_data = []

    for _ in range(5):
        train_data.append(load_and_prepare_data(directory))

    training_results = {}

    for model_name in SMALL_MODELS:

        print(f"\n{'-'*30}")
        print(f"Training {model_name}...")
        print(f"{'-'*30}\n")

        training_results[model_name] = []

        for i in range(5):

            X_train, X_val, y_train, y_val = train_data[i]

            model = get_model(model_name)

            model.fit(
                X_train, y_train,
                epochs=30, batch_size=8,
                validation_data=(X_val, y_val),
                verbose=0
            )

            y_pred_proba = model.predict(X_val)

            y_pred = (y_pred_proba > 0.5).astype(int)

            metrics = calc_metrics(y_val, y_pred)

            training_results[model_name].append(metrics)

            del model

    pretty_print_metrics(training_results, directory)

    return training_results


def save_csv(data):
    metrics = ["roc_auc", "f1_score", "recall", "precision", "accuracy"]

    for metric in metrics:
        rows_m_models = []
        rows_m_words = []

        for word, models in data.items():
            for model_name, training_metrics in models.items():
                avg_metric = 0

                for metrics in training_metrics:
                    avg_metric += metrics[metric]

                avg_metric /= len(training_metrics)

                rows_m_models.append(
                    {
                        "word": word,
                        model_name: avg_metric
                    }
                )

                rows_m_words.append({
                    "model": model_name,
                    word: avg_metric
                })

        for info in [[rows_m_models, "word", "models"], [rows_m_words, "model", "words"]]:
            rows, group_by, name = info

            df = pd.DataFrame(rows)
            df_grouped = df.groupby(group_by).first().reset_index()
            output_file = f"results/results_{metric}_{name}.csv"

            if os.path.exists(output_file):
                if name == "models":
                    print(f"Model file {output_file}")
                    df_grouped.to_csv(output_file, mode='a', header=False, index=False)
                    continue

                saved_df = pd.read_csv(output_file)
                df_grouped = df_grouped.drop("model", axis=1)
                df_grouped = pd.concat([saved_df, df_grouped], axis=1)

            df_grouped.to_csv(output_file, index=False)


def main(words):
    metrics_results = {}

    for dir in words:
        word_metrics = train(dir)
        metrics_results[dir] = word_metrics

    save_csv(metrics_results)


# ----------------------------------------------------------------------------------------
if __name__ == "__main__":
    # main(['dia'])

    data = {
        'aaa': {
            'MLPClassifier': [
                {
                    'roc_auc': 0.7,
                    'f1_score': 0.7,
                    'recall': 0.7,
                    'precision': 0.7,
                    'accuracy': 0.7
                }
            ],
            'LSTM': [
                {
                    'roc_auc': 0.7,
                    'f1_score': 0.7,
                    'recall': 0.7,
                    'precision': 0.7,
                    'accuracy': 0.7
                }
            ]
        },
        'bbb': {
            'MLPClassifier': [
                {
                    'roc_auc': 0.5,
                    'f1_score': 0.5,
                    'recall': 0.5,
                    'precision': 0.5,
                    'accuracy': 0.5
                }
            ],
            'LSTM': [
                {
                    'roc_auc': 0.5,
                    'f1_score': 0.5,
                    'recall': 0.5,
                    'precision': 0.5,
                    'accuracy': 0.5
                }
            ]
        }
    }

    save_csv(data)

    data = {
        'ccc': {
            'MLPClassifier': [
                {
                    'roc_auc': 0.6,
                    'f1_score': 0.6,
                    'recall': 0.6,
                    'precision': 0.6,
                    'accuracy': 0.6
                }
            ],
            'LSTM': [
                {
                    'roc_auc': 0.7,
                    'f1_score': 0.7,
                    'recall': 0.7,
                    'precision': 0.7,
                    'accuracy': 0.7
                }
            ]
        },
        'ddd': {
            'MLPClassifier': [
                {
                    'roc_auc': 0.6,
                    'f1_score': 0.6,
                    'recall': 0.6,
                    'precision': 0.6,
                    'accuracy': 0.6
                }
            ],
            'LSTM': [
                {
                    'roc_auc': 0.5,
                    'f1_score': 0.5,
                    'recall': 0.5,
                    'precision': 0.5,
                    'accuracy': 0.5
                }
            ]
        }
    }

    save_csv(data)
