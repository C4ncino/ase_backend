from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model


def get_LSTM_v1() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.LSTM(38, return_sequences=True),
        layers.Dropout(0.1),
        layers.LSTM(16),
        layers.Dropout(0.2),
        layers.Dense(8, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])


def get_LSTM_v2() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.LSTM(36, return_sequences=True),
        layers.Dropout(0.1),
        layers.LSTM(16),
        layers.Dropout(0.2),
        layers.Dense(8, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])


def get_LSTM_v3() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.LSTM(36, return_sequences=True),
        layers.Dropout(0.1),
        layers.LSTM(16),
        layers.Dropout(0.3),
        layers.Dense(8, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(1, activation='sigmoid')
    ])


def get_LSTM_v4() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.LSTM(20, return_sequences=True),
        layers.Dropout(0.1),
        layers.LSTM(30),
        layers.Dropout(0.2),
        layers.Dense(10, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(1, activation='sigmoid')
    ])


def get_LSTM_v5() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.LSTM(38, return_sequences=True),
        layers.Dropout(0.1),
        layers.LSTM(16),
        layers.Dropout(0.2),
        layers.Dense(10, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU_v1() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.GRU(16, return_sequences=True),
        layers.Dropout(0.4),
        layers.GRU(32),
        layers.Dropout(0.4),
        layers.Dense(4, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU_v2() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.GRU(32, return_sequences=True),
        layers.Dropout(0.2),
        layers.GRU(8),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU_v3() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.GRU(32, return_sequences=True),
        layers.Dropout(0.4),
        layers.GRU(8),
        layers.Dropout(0.4),
        layers.Dense(16, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU_v4() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.GRU(32, return_sequences=True),
        layers.Dropout(0.2),
        layers.GRU(8),
        layers.Dropout(0.2),
        layers.Dense(8, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU_v5() -> Model:
    return Sequential([
        layers.Input(shape=(60, 8)),
        layers.GRU(16, return_sequences=True),
        layers.Dropout(0.1),
        layers.GRU(12),
        layers.Dropout(0.5),
        layers.Dense(16, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid')
    ])


def get_model(type: str) -> Model:
    model = None

    match type:
        case 'L1':
            model = get_LSTM_v1()
        case 'L2':
            model = get_LSTM_v2()
        case 'L3':
            model = get_LSTM_v3()
        case 'L4':
            model = get_LSTM_v4()
        case 'L5':
            model = get_LSTM_v5()
        case 'G1':
            model = get_GRU_v1()
        case 'G2':
            model = get_GRU_v2()
        case 'G3':
            model = get_GRU_v3()
        case 'G4':
            model = get_GRU_v4()
        case 'G5':
            model = get_GRU_v5()

    if model:
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    return model
