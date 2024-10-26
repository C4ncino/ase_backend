from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model


def get_large_LSTM_v1() -> Model:
    return Sequential([
        layers.Input(shape=(55, 8)),
        layers.LSTM(256, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(128, return_sequences=True),
        layers.Dropout(0.3),
        layers.LSTM(64),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
    ])


def get_large_model(type: str, n_classes: int) -> Model:
    model = None

    match type:
        case 'L1':
            model = get_large_LSTM_v1()

    if model:
        model.add(layers.Dense(n_classes, activation='softmax'))

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

    return model
