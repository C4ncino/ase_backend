import {train, layers, sequential} from "@tensorflow/tfjs";
import {InputConfig, Initializers } from "./utils.js"

export const SMALL_MODEL_POOL = [
  "G3",
  "G4",
  "G5",
  "G2",
  "G1",
  "L4",
  "L3",
  "L1",
  "L2",
  "L5",
];

const get_LSTM_v1 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 38, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.1 }),
      layers.lstm({ units: 16, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 8, activation: "relu" }),
      layers.dropout({ rate: 0.3 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v2 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 36, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.1 }),
      layers.lstm({ units: 16, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 8, activation: "relu" }),
      layers.dropout({ rate: 0.3 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v3 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 36, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.1 }),
      layers.lstm({ units: 16, ...Initializers }),
      layers.dropout({ rate: 0.3 }),
      layers.dense({ units: 8, activation: "relu" }),
      layers.dropout({ rate: 0.4 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v4 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 20, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.1 }),
      layers.lstm({ units: 30, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 10, activation: "relu" }),
      layers.dropout({ rate: 0.4 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_LSTM_v5 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 38, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.1 }),
      layers.lstm({ units: 16, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 10, activation: "relu" }),
      layers.dropout({ rate: 0.4 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v1 = () => {
  return sequential({
    layers: [
      layers.gru({ units: 16, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.4 }),
      layers.gru({ units: 32, ...Initializers }),
      layers.dropout({ rate: 0.4 }),
      layers.dense({ units: 4, activation: "relu" }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v2 = () => {
  return sequential({
    layers: [
      layers.gru({ units: 32, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.2 }),
      layers.gru({ units: 8, ...Initializers }),
      layers.dropout({ rate: 0.3 }),
      layers.dense({ units: 32, activation: "relu" }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v3 = () => {
  return sequential({
    layers: [
      layers.gru({ units: 32, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.4 }),
      layers.gru({ units: 8, ...Initializers }),
      layers.dropout({ rate: 0.4 }),
      layers.dense({ units: 16, activation: "relu" }),
      layers.dropout({ rate: 0.3 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v4 = () => {
  return sequential({
    layers: [
      layers.gru({ units: 32, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.2 }),
      layers.gru({ units: 8, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 8, activation: "relu" }),
      layers.dropout({ rate: 0.5 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
    ],
  });
};

const get_GRU_v5 = () => {
  return sequential({
    layers: [
      layers.gru({ units: 16, ...InputConfig, ...Initializers}),
      layers.dropout({ rate: 0.1 }),
      layers.gru({ units: 12, ...Initializers }),
      layers.dropout({ rate: 0.5 }),
      layers.dense({ units: 16, activation: "relu" }),
      layers.dropout({ rate: 0.2 }),
      layers.dense({ units: 1, activation: "sigmoid" }),
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

  const initLR = 0.001;
  const initMomentum = 0.9;
  const optimizer = train.momentum(initLR, initMomentum);

  model.compile({
    optimizer,
    loss: "binaryCrossentropy",
    metrics: ["accuracy"],
  });

  return model;
};
