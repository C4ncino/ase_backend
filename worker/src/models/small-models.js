import { train, layers, sequential } from "@tensorflow/tfjs";
import { InputConfig, Initializers, InputShape } from "./utils.js";

export const SMALL_MODELS_POOL = [
  "G1",
  "L2",
  "G2",
  "D1",
  "G5",
  "G3",
  "G4",
  "D2",
  "D3",
];

const ModelsConfig = {
  L1: { l1: 24, d1: 0.4, l2: 24, d2: 0.2, l3: 14, d3: 0.1 },
  L2: { l1: 20, d1: 0.1, l2: 30, d2: 0.2, l3: 10, d3: 0.4 },
  L3: { l1: 30, d1: 0.4, l2: 20, d2: 0.2, l3: 18, d3: 0.1 },
  // ----------------------------------------------------------
  G2: { l1: 16, d1: 0.3, l2: 24, d2: 0.1, l3: 20, d3: 0.2 },
  G5: { l1: 10, d1: 0.4, l2: 24, d2: 0.1, l3: 20, d3: 0.2 },
  G3: { l1: 14, d1: 0.3, l2: 24, d2: 0.1, l3: 20, d3: 0.2 },
  G4: { l1: 14, d1: 0.3, l2: 24, d2: 0.1, l3: 20, d3: 0.3 },
  G1: { l1: 24, d1: 0.3, l2: 18, d2: 0.3, l3: 24, d3: 0.2 },
  G6: { l1: 32, d1: 0.2, l2: 8, d2: 0.3, l3: 32, d3: 0.2 },
  // ----------------------------------------------------------
  D2: { l1: 30, d1: 0.4, l2: 16, d2: 0.3, l3: 22, d3: 0.1 },
  D1: { l1: 24, d1: 0.2, l2: 20, d2: 0.3, l3: 20, d3: 0.1 },
  D3: { l1: 30, d1: 0.4, l2: 24, d2: 0.3, l3: 16, d3: 0.1 },
};

const get_LSTM = (config) => {
  return sequential({
    layers: [
      layers.lstm({ units: config.l1, ...InputConfig, ...Initializers }),
      layers.dropout({ rate: config.d1 }),
      layers.lstm({ units: config.l2, ...Initializers }),
      layers.dropout({ rate: config.d2 }),
      layers.dense({ units: config.l3, activation: "relu" }),
      layers.dropout({ rate: config.d3 }),
    ],
  });
};

const get_GRU = (config) => {
  return sequential({
    layers: [
      layers.gru({ units: config.l1, ...InputConfig, ...Initializers }),
      layers.dropout({ rate: config.d1 }),
      layers.gru({ units: config.l2, ...Initializers }),
      layers.dropout({ rate: config.d2 }),
      layers.dense({ units: config.l3, activation: "relu" }),
      layers.dropout({ rate: config.d3 }),
    ],
  });
};

const get_Dense = (config) => {
  return sequential({
    layers: [
      layers.flatten({ inputShape: InputShape }),
      layers.dense({ units: config.l1, activation: "relu" }),
      layers.dropout({ rate: config.d1 }),
      layers.dense({ units: config.l2, activation: "relu" }),
      layers.dropout({ rate: config.d2 }),
      layers.dense({ units: config.l3, activation: "relu" }),
      layers.dropout({ rate: config.d3 }),
    ],
  });
};

export const getModel = async (type) => {
  let model = undefined;

  switch (type[0]) {
    case "L":
      model = get_LSTM(ModelsConfig[type]);
      break;

    case "G":
      model = get_GRU(ModelsConfig[type]);
      break;

    case "D":
      model = get_Dense(ModelsConfig[type]);
      break;
  }

  model.add(layers.dense({ units: 1, activation: "sigmoid" }));

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
