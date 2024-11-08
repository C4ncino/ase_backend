import { sequential, layers, train } from "@tensorflow/tfjs";
import { InputConfig, Initializers } from "./utils.js";

const get_large_LSTM_v1 = () => {
  return sequential({
    layers: [
      layers.lstm({ units: 96, ...InputConfig, ...Initializers }),
      layers.dropout({ rate: 0.2 }),
      layers.lstm({ units: 64, ...Initializers }),
      layers.dropout({ rate: 0.1 }),
      layers.dense({ units: 128, activation: "relu" }),
      layers.dropout({ rate: 0.2 }),
    ],
  });
};

export const get_large_model = (type, nClases) => {
  let model = null;

  switch (type) {
    case "L1":
      model = get_large_LSTM_v1();
      break;
  }

  if (model) {
    model.add(layers.dense({ units: nClases, activation: "softmax" }));

    const initLR = 0.005;
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
