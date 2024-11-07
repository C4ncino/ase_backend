import { sequential, layers, train } from "@tensorflow/tfjs";
import { InputConfig, Initializers } from "./utils.js";

const get_large_LSTM_v1 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 172, ...InputConfig, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.lstm({ units: 96, returnSequences: true, ...Initializers }),
      layers.dropout({ rate: 0.3 }),
      layers.lstm({ units: 64, ...Initializers }),
      layers.dropout({ rate: 0.3 }),
      layers.dense({ units: 128, activation: "relu" }),
      layers.dropout({ rate: 0.3 }),
    ],
  });
};

export const get_large_model = (type, n_classes) => {
  let model = null;

  switch (type) {
    case "L1":
      model = get_large_LSTM_v1();
      break;
  }

  if (model) {
    model.add(layers.dense({ units: n_classes, activation: "softmax" }));

    const initLR = 0.001;
    const initMomentum = 0.9;
    const optimizer = train.momentum(initLR, initMomentum);

    model.compile({
      optimizer,
      loss: "sparseCategoricalCrossentropy",
      metrics: ["accuracy"],
    });
  }

  return model;
};
