from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model


def get_LSTM_model() -> Model:

    return Sequential([
        layers.LSTM(32, input_shape=(55, 8), return_sequences=True),
        layers.LSTM(16),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU_model() -> Model:

    return Sequential([
        layers.GRU(32, input_shape=(55, 8), return_sequences=True),
        layers.GRU(16),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])


def get_model(type: str) -> Model:
    model = None

    if type == 'LSTM':
        model = get_LSTM_model()
    elif type == 'GRU':
        model = get_GRU_model()

    if model:
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    return model
