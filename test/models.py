from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Model


recurrent_config = {
    'kernel_initializer': 'he_normal',
    'recurrent_initializer': 'he_normal'
}

input_layer_config = {
    'input_shape': (60, 8),
    'return_sequences': True,
    **recurrent_config
}

GRU_CONFIGS = [
    {"layer1": 24, "dropout1": 0.3, "layer2": 18, "dropout2": 0.3, "dense": 24, "dropout3": 0.2},
    {"layer1": 16, "dropout1": 0.3, "layer2": 24, "dropout2": 0.1, "dense": 20, "dropout3": 0.2},
    {"layer1": 14, "dropout1": 0.3, "layer2": 24, "dropout2": 0.1, "dense": 20, "dropout3": 0.2},
    {"layer1": 14, "dropout1": 0.3, "layer2": 24, "dropout2": 0.1, "dense": 20, "dropout3": 0.3},
    {"layer1": 10, "dropout1": 0.4, "layer2": 24, "dropout2": 0.1, "dense": 20, "dropout3": 0.2},
    {"layer1": 14, "dropout1": 0.4, "layer2": 8,  "dropout2": 0.2, "dense": 24, "dropout3": 0.1},
    {"layer1": 14, "dropout1": 0.4, "layer2": 10, "dropout2": 0.2, "dense": 20, "dropout3": 0.1},
    {"layer1": 16, "dropout1": 0.2, "layer2": 10, "dropout2": 0.3, "dense": 16, "dropout3": 0.3},

    {"layer1": 16, "dropout1": 0.4, "layer2": 32, "dropout2": 0.4, "dense": 4, "dropout3": 0.2},
    {"layer1": 32, "dropout1": 0.2, "layer2": 8, "dropout2": 0.3, "dense": 32, "dropout3": 0.2},
    {"layer1": 32, "dropout1": 0.4, "layer2": 8, "dropout2": 0.4, "dense": 16, "dropout3": 0.3},
    {"layer1": 32, "dropout1": 0.2, "layer2": 8, "dropout2": 0.2, "dense": 8, "dropout3": 0.5},
    {"layer1": 16, "dropout1": 0.1, "layer2": 12, "dropout2": 0.5, "dense": 16, "dropout3": 0.2},
]

LSTM_CONFIGS = [
    {"layer1": 24, "dropout1": 0.4, "layer2": 24, "dropout2": 0.2, "dense": 14, "dropout3": 0.1},
    {"layer1": 24, "dropout1": 0.4, "layer2": 20, "dropout2": 0.4, "dense": 16, "dropout3": 0.1},
    {"layer1": 20, "dropout1": 0.4, "layer2": 18, "dropout2": 0.4, "dense": 18, "dropout3": 0.1},
    {"layer1": 24, "dropout1": 0.4, "layer2": 20, "dropout2": 0.3, "dense": 20, "dropout3": 0.1},

    {"layer1": 38, "dropout1": 0.1, "layer2": 16, "dropout2": 0.2, "dense": 8, "dropout3": 0.3},
    {"layer1": 36, "dropout1": 0.1, "layer2": 16, "dropout2": 0.2, "dense": 8, "dropout3": 0.3},
    {"layer1": 36, "dropout1": 0.1, "layer2": 16, "dropout2": 0.2, "dense": 8, "dropout3": 0.4},
    {"layer1": 20, "dropout1": 0.1, "layer2": 30, "dropout2": 0.2, "dense": 10, "dropout3": 0.4},
    {"layer1": 38, "dropout1": 0.1, "layer2": 16, "dropout2": 0.2, "dense": 10, "dropout3": 0.4},

    {"layer1": 24, "dropout1": 0.2, "layer2": 20, "dropout2": 0.3, "dense": 20, "dropout3": 0.1},
    {"layer1": 18, "dropout1": 0.4, "layer2": 16, "dropout2": 0.2, "dense": 10, "dropout3": 0.1},
    {"layer1": 30, "dropout1": 0.4, "layer2": 20, "dropout2": 0.2, "dense": 18, "dropout3": 0.1},
    {"layer1": 28, "dropout1": 0.4, "layer2": 16, "dropout2": 0.2, "dense": 20, "dropout3": 0.1},
    {"layer1": 28, "dropout1": 0.4, "layer2": 20, "dropout2": 0.3, "dense": 24, "dropout3": 0.1},
    {"layer1": 28, "dropout1": 0.2, "layer2": 16, "dropout2": 0.3, "dense": 16, "dropout3": 0.1}
]

# SMALL_MODELS = [
#     "L1", "L2", "L3", "L4",
#     "LG1", "LG2", "LG3", "LG4", "LG5",
#     "G1", "G2", "G3", "G4", "G5",
#     "G6", "G7", "G8",
#     "GG1", "GG2", "GG3", "GG4", "GG5",
# ]

SMALL_MODELS = [
    "L21", "L22", "L23", "L24", "L25", "L26"
    "G1", "G2", "G4", "G3", "L2", "L1",
    "LG5", "GG5", "L4", "G8", "G5", "LG1",
    "GG4", "GG2", "LG4", "L3", "LG3"
]


def get_LSTM(config: dict) -> Model:
    return Sequential([
        layers.LSTM(config["layer1"], **input_layer_config),
        layers.Dropout(config["dropout1"]),
        layers.LSTM(config["layer2"], **recurrent_config),
        layers.Dropout(config["dropout2"]),
        layers.Dense(config["dense"], activation='relu'),
        layers.Dropout(config["dropout3"]),
        layers.Dense(1, activation='sigmoid')
    ])


def get_GRU(config: dict) -> Model:
    return Sequential([
        layers.GRU(config["layer1"], **input_layer_config),
        layers.Dropout(config["dropout1"]),
        layers.GRU(config["layer2"], **recurrent_config),
        layers.Dropout(config["dropout2"]),
        layers.Dense(config["dense"], activation='relu'),
        layers.Dropout(config["dropout3"]),
        layers.Dense(1, activation='sigmoid')
    ])


def get_model(type: str) -> Model:
    model = None

    match type:
        case 'L1':
            model = get_LSTM(LSTM_CONFIGS[0])
        case 'L2':
            model = get_LSTM(LSTM_CONFIGS[1])
        case 'L3':
            model = get_LSTM(LSTM_CONFIGS[2])
        case 'L4':
            model = get_LSTM(LSTM_CONFIGS[3])
        case 'LG1':
            model = get_LSTM(LSTM_CONFIGS[4])
        case 'LG2':
            model = get_LSTM(LSTM_CONFIGS[5])
        case 'LG3':
            model = get_LSTM(LSTM_CONFIGS[6])
        case 'LG4':
            model = get_LSTM(LSTM_CONFIGS[7])
        case 'LG5':
            model = get_LSTM(LSTM_CONFIGS[8])
        
        case 'L21':
            model = get_LSTM(LSTM_CONFIGS[9])
        case 'L22':
            model = get_LSTM(LSTM_CONFIGS[10])
        case 'L23':
            model = get_LSTM(LSTM_CONFIGS[11])
        case 'L24':
            model = get_LSTM(LSTM_CONFIGS[12])
        case 'L25':
            model = get_LSTM(LSTM_CONFIGS[13])
        case 'L26':
            model = get_LSTM(LSTM_CONFIGS[14])

        case 'G1':
            model = get_GRU(GRU_CONFIGS[0])
        case 'G2':
            model = get_GRU(GRU_CONFIGS[1])
        case 'G3':
            model = get_GRU(GRU_CONFIGS[2])
        case 'G4':
            model = get_GRU(GRU_CONFIGS[3])
        case 'G5':
            model = get_GRU(GRU_CONFIGS[4])
        case 'G6':
            model = get_GRU(GRU_CONFIGS[5])
        case 'G7':
            model = get_GRU(GRU_CONFIGS[6])
        case 'G8':
            model = get_GRU(GRU_CONFIGS[7])
        case 'GG1':
            model = get_GRU(GRU_CONFIGS[8])
        case 'GG2':
            model = get_GRU(GRU_CONFIGS[9])
        case 'GG3':
            model = get_GRU(GRU_CONFIGS[10])
        case 'GG4':
            model = get_GRU(GRU_CONFIGS[11])
        case 'GG5':
            model = get_GRU(GRU_CONFIGS[12])

    if model:
        optimizer = SGD(learning_rate=0.001, momentum=0.9)

        model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

    return model
