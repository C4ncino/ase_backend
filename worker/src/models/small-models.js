import { train, layers, sequential } from "@tensorflow/tfjs";
import { InputConfig, Initializers } from "./utils.js";

export const SMALL_MODELS_POOL = [
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

const ModelsConfig = {
  L1: { l1: 38, d1: 0.1, l2: 16, d2: 0.2, l3: 8, d3: 0.3 },
  L2: { l1: 36, d1: 0.1, l2: 16, d2: 0.2, l3: 8, d3: 0.3 },
  L3: { l1: 36, d1: 0.1, l2: 16, d2: 0.3, l3: 8, d3: 0.4 },
  L4: { l1: 20, d1: 0.1, l2: 30, d2: 0.2, l3: 10, d3: 0.4 },
  L5: { l1: 38, d1: 0.1, l2: 16, d2: 0.2, l3: 10, d3: 0.4 },
  // ----------------------------------------------------------
  G1: { l1: 16, d1: 0.4, l2: 32, d2: 0.4, l3: 4, d3: 0.2 },
  G2: { l1: 32, d1: 0.2, l2: 8, d2: 0.3, l3: 32, d3: 0.2 },
  G3: { l1: 32, d1: 0.4, l2: 8, d2: 0.4, l3: 16, d3: 0.3 },
  G4: { l1: 32, d1: 0.2, l2: 8, d2: 0.2, l3: 8, d3: 0.5 },
  G5: { l1: 16, d1: 0.1, l2: 12, d2: 0.5, l3: 16, d3: 0.2 },
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

export const getModel = async (type) => {
  let model = undefined;

  model =
    type[0] === "L"
      ? get_LSTM(ModelsConfig[type])
      : get_GRU(ModelsConfig[type]);

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
