import { getModel, SMALL_MODEL_POOL } from "../models/small-models.js";
import { calculateMetrics, hasBetterMetrics, createEarlyStoppingCallback } from "../models/metrics.js";
import { getModelInfo } from "../models/save-model.js"
import { tensor } from "@tensorflow/tfjs";
import { minimizeModel } from "../models/minimizer.js"
import { calculateBatchSize, logMetrics } from "../models/utils.js";

export const trainModels = async (trainingData, dbInfo, sensorData) => {
  let bestModel = null;
  let bestMetrics = null;

  const { xTrain, xVal, yTrain, yVal } = trainingData;

  console.log(xTrain.length, xVal.length, yTrain.length, yVal.length);

  const batchSize = calculateBatchSize(xTrain.length);

  console.log(`Batch size: ${batchSize}`);
  
  const xTensor = tensor(xTrain);
  const yTensor = tensor(yTrain);
  const xValTensor = tensor(xVal);
  const yValTensor = tensor(yVal);

  for (const modelVersion of SMALL_MODEL_POOL) {
    const model = await getModel(modelVersion);

    const callBack = createEarlyStoppingCallback(model)

    await model.fit(xTensor, yTensor, {
      epochs: 20,
      batchSize: batchSize,
      validationData: [xValTensor, yValTensor],
      callbacks: [callBack]
      // verbose: 0,
    });

    const minModel = minimizeModel(model);

    const yPredProb = minModel.predict(xValTensor).dataSync();
    const yPred = yPredProb.map((prob) => (prob > 0.5 ? 1 : 0));

    const metrics = calculateMetrics(yValTensor.dataSync(), yPred);

    if (metrics.roc_auc > 0.85) {
      bestModel = model;
      bestMetrics = metrics;
      break;
    }

    if (!bestMetrics) {
      bestModel = model;
      bestMetrics = metrics;
      continue;
    }

    if (hasBetterMetrics(metrics, bestMetrics)) {
      bestModel.dispose();
      bestModel = model;
      bestMetrics = metrics;
      continue;
    }
    else {
      model.dispose();
    }

  }

  bestModel.summary();

  logMetrics(bestMetrics);

  const modelInfo = await getModelInfo(bestModel);

  dbInfo.model = modelInfo;

  return [dbInfo, sensorData];
};
