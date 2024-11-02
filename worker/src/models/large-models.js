import * as tf from "@tensorflow/tfjs";

const SHAPE = [60, 8];

const INPUT_CONFIG = {
  returnSequences: true,
  inputShape: SHAPE,
  kernelInitializer: "randomNormal",
  recurrentInitializer: "randomNormal",
}

const get_large_LSTM_v1 = () => {
  return tf.sequential({
    layers: [
      tf.layers.lstm({ units: 256, ...INPUT_CONFIG }),
      tf.layers.dropout({ rate: 0.2 }),
      tf.layers.lstm({ units: 128, returnSequences: true }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.lstm({ units: 64 }),
      tf.layers.dropout({ rate: 0.3 }),
      tf.layers.dense({ units: 128, activation: "relu" }),
      tf.layers.dropout({ rate: 0.4 }),
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
    model.add(tf.layers.dense({ units: n_classes, activation: "softmax" }));

    model.compile({
      optimizer: "adam",
      loss: "sparseCategoricalCrossentropy",
      metrics: ["accuracy"],
    });
  }

  return model;
};
