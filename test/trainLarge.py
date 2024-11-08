import os
import numpy as np
import pandas as pd

from sklearn.metrics import recall_score, f1_score, roc_auc_score
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score

from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical

from prepare_data import load_and_prepare_data_lg


def calc_metrics(y_true, y_pred, y_pred_proba):
    y_true_one_hot = to_categorical(y_true)

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average='macro'),
        "recall": recall_score(y_true, y_pred, average='macro'),
        "f1_score": f1_score(y_true, y_pred, average='macro'),
        "roc_auc": roc_auc_score(y_true_one_hot, y_pred_proba, multi_class='ovr'),
        "roc_auc_ovo": roc_auc_score(y_true_one_hot, y_pred_proba, multi_class='ovo'),
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


def train():

    train_data = []

    for _ in range(5):
        train_data.append(load_and_prepare_data_lg())

    training_results = {}

    print(f"\n{'-'*30}")
    print("Training...")
    print(f"{'-'*30}\n")

    training_results["LSTM1"] = []

    for i in range(5):

        X_train, X_val, y_train, y_val = train_data[i]

        input_config = {
            "return_sequences": True,
            "input_shape": (60, 8),
        }

        initializers = {
            "kernel_initializer": "he_normal",
            "recurrent_initializer": "he_normal",
        }

        model = Sequential([
            layers.GRU(172, **input_config, **initializers),
            layers.Dropout(0.2),
            layers.GRU(96, return_sequences=True, **initializers),
            layers.Dropout(0.1),
            layers.GRU(64, **initializers),
            layers.Dropout(0.1),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.2),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(21, activation="softmax")
        ])

        init_lr = 0.001
        init_momentum = 0.9
        optimizer = SGD(learning_rate=init_lr, momentum=init_momentum)

        model.compile(
            optimizer=optimizer,
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

        model.fit(
            X_train, y_train,
            epochs=50, batch_size=16,
            validation_data=(X_val, y_val),
        )

        y_pred_proba = model.predict(X_val)

        y_pred = np.argmax(y_pred_proba, axis=1)

        metrics = calc_metrics(y_val, y_pred, y_pred_proba)

        training_results["LSTM1"].append(metrics)

        del model

    pretty_print_metrics(training_results, "all")

    return training_results


def save_csv(data):
    metrics = ["roc_auc", "roc_auc_ovo",  "f1_score", "recall", "precision", "accuracy"]

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


def main():
    metrics_results = {}

    word_metrics = train()
    metrics_results["All"] = word_metrics

    save_csv(metrics_results)


# ----------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

    # data = {
    #     'aaa': {
    #         'MLPClassifier': [
    #             {
    #                 'roc_auc': 0.7,
    #                 'f1_score': 0.7,
    #                 'recall': 0.7,
    #                 'precision': 0.7,
    #                 'accuracy': 0.7
    #             }
    #         ],
    #         'LSTM': [
    #             {
    #                 'roc_auc': 0.7,
    #                 'f1_score': 0.7,
    #                 'recall': 0.7,
    #                 'precision': 0.7,
    #                 'accuracy': 0.7
    #             }
    #         ]
    #     },
    #     'bbb': {
    #         'MLPClassifier': [
    #             {
    #                 'roc_auc': 0.5,
    #                 'f1_score': 0.5,
    #                 'recall': 0.5,
    #                 'precision': 0.5,
    #                 'accuracy': 0.5
    #             }
    #         ],
    #         'LSTM': [
    #             {
    #                 'roc_auc': 0.5,
    #                 'f1_score': 0.5,
    #                 'recall': 0.5,
    #                 'precision': 0.5,
    #                 'accuracy': 0.5
    #             }
    #         ]
    #     }
    # }

    # save_csv(data)

    # data = {
    #     'ccc': {
    #         'MLPClassifier': [
    #             {
    #                 'roc_auc': 0.6,
    #                 'f1_score': 0.6,
    #                 'recall': 0.6,
    #                 'precision': 0.6,
    #                 'accuracy': 0.6
    #             }
    #         ],
    #         'LSTM': [
    #             {
    #                 'roc_auc': 0.7,
    #                 'f1_score': 0.7,
    #                 'recall': 0.7,
    #                 'precision': 0.7,
    #                 'accuracy': 0.7
    #             }
    #         ]
    #     },
    #     'ddd': {
    #         'MLPClassifier': [
    #             {
    #                 'roc_auc': 0.6,
    #                 'f1_score': 0.6,
    #                 'recall': 0.6,
    #                 'precision': 0.6,
    #                 'accuracy': 0.6
    #             }
    #         ],
    #         'LSTM': [
    #             {
    #                 'roc_auc': 0.5,
    #                 'f1_score': 0.5,
    #                 'recall': 0.5,
    #                 'precision': 0.5,
    #                 'accuracy': 0.5
    #             }
    #         ]
    #     }
    # }

    # save_csv(data)
