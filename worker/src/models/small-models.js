import * as tf from "@tensorflow/tfjs";

const SHAPE = [60, 8];

const INPUT_CONFIG = {
  returnSequences: true,
  inputShape: SHAPE,
  kernelInitializer: "randomNormal",
  recurrentInitializer: "randomNormal",
}

export const SMALL_MODEL_POOL = [
  "L1",
  "L2",
  "L3",
  "L4",
  "L5",
  "G1",
  "G2",
  "G3",
  "G4",
  "G5",
];

const get_LSTM_v1 = () => {
  return tf.sequential({
    layers: [
      tf.layers.lstm({ units: 38, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.1 }),
      tf.layers.lstm({ units: 16 }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 8, activation: "relu" }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v2 = () => {
  return tf.sequential({
    layers: [
      tf.layers.lstm({ units: 36, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.1 }),
      tf.layers.lstm({ units: 16 }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 8, activation: "relu" }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v3 = () => {
  return tf.sequential({
    layers: [
      tf.layers.lstm({ units: 36, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.1 }),
      tf.layers.lstm({ units: 16 }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.dense({ units: 8, activation: "relu" }),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v4 = () => {
  return tf.sequential({
    layers: [
      tf.layers.lstm({ units: 20, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.1 }),
      tf.layers.lstm({ units: 30 }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 10, activation: "relu" }),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v5 = () => {
  return tf.sequential({
    layers: [
      tf.layers.lstm({ units: 38, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.1 }),
      tf.layers.lstm({ units: 16 }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 10, activation: "relu" }),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

// Modelos GRU traducidos con inputShape eSHAPEcapa

const get_GRU_v1 = () => {
  return tf.sequential({
    layers: [
      tf.layers.gru({ units: 16, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.gru({ units: 32 }),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.dense({ units: 4, activation: "relu" }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v2 = () => {
  return tf.sequential({
    layers: [
      tf.layers.gru({ units: 32, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.gru({ units: 8 }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.dense({ units: 32, activation: "relu" }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v3 = () => {
  return tf.sequential({
    layers: [
      tf.layers.gru({ units: 32, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.gru({ units: 8 }),
      tf.layers.dropout({ rate: 0.4 }),
      tf.layers.dense({ units: 16, activation: "relu" }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v4 = () => {
  return tf.sequential({
    layers: [
      tf.layers.gru({ units: 32, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.gru({ units: 8 }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 8, activation: "relu" }),
      tf.layers.dropout({ rate: 0.5 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v5 = () => {
  return tf.sequential({
    layers: [
      tf.layers.gru({ units: 16, ...INPUT_CONFIG}),
      tf.layers.dropout({ rate: 0.1 }),
      tf.layers.gru({ units: 12 }),
      tf.layers.dropout({ rate: 0.5 }),
      tf.layers.dense({ units: 16, activation: "relu" }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

export const getModel = async (type) => {
  let model = undefined;

  switch (type) {
    case "L1":
      model = get_LSTM_v1();
      break;
    case "L2":
      model = get_LSTM_v2();
      break;
    case "L3":
      model = get_LSTM_v3();
      break;
    case "L4":
      model = get_LSTM_v4();
      break;
    case "L5":
      model = get_LSTM_v5();
      break;
    case "G1":
      model = get_GRU_v1();
      break;
    case "G2":
      model = get_GRU_v2();
      break;
    case "G3":
      model = get_GRU_v3();
      break;
    case "G4":
      model = get_GRU_v4();
      break;
    case "G5":
      model = get_GRU_v5();
      break;
    default:
      model = get_LSTM_v1();
      break;
  }

  await model.compile({
    optimizer: tf.train.adam(0.001),
    loss: "binaryCrossentropy",
    metrics: ["accuracy"],
  });

  return model;
};
