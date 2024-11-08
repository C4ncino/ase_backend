import { get_large_model } from "../models/large-models.js";
import { tensor } from "@tensorflow/tfjs";
import { getModelInfo } from "../models/save-model.js";
import { calculateBatchSize } from "../models/utils.js";
import { createEarlyStoppingCallback } from "../models/metrics.js";

export const trainLargeModel = async (trainingData, nClases, userId) => {
  const { xTrain, xVal, yTrain, yVal } = trainingData;

  console.log(xTrain.length, xVal.length, yTrain.length, yVal.length);

  const xTensor = tensor(xTrain);
  const yTensor = tensor(yTrain);
  const xValTensor = tensor(xVal);
  const yValTensor = tensor(yVal);

  const batchSize = calculateBatchSize(xTrain.length);

  const model = get_large_model("L1", nClases);

  const callBack = createEarlyStoppingCallback(model);

  await model.fit(xTensor, yTensor, {
    epochs: 50,
    batchSize: batchSize,
    validationData: [xValTensor, yValTensor],
    callbacks: [callBack],
    // verbose: 0,
  });

  model.summary();

  const modelInfo = await getModelInfo(model);

  return [modelInfo, userId];
};
