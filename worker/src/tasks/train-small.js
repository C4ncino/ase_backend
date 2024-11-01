import { getModel, SMALL_MODEL_POOL } from "../models/small-models.js";
import { calculateMetrics, hasBetterMetrics } from "../models/metrics.js";
import { getModelInfo } from "../models/save-model.js"
import {tensor} from "@tensorflow/tfjs";

export const trainModels = async (trainingData, dbInfo, sensorData) => {
  let bestModel = null;
  let bestMetrics = null;

  const { xTrain, xVal, yTrain, yVal } = trainingData;

  console.log(xTrain.length, xVal.length, yTrain.length, yVal.length);
  
  const xTensor = tensor(xTrain);
  const yTensor = tensor(yTrain);
  const xValTensor = tensor(xVal);
  const yValTensor = tensor(yVal);

  for (const modelVersion of SMALL_MODEL_POOL) {
    const model = await getModel(modelVersion);

    await model.fit(xTensor, yTensor, {
      epochs: 20,
      batchSize: 8,
      validationData: [xValTensor, yValTensor],
      verbose: 0,
    });

    const yPredProb = model.predict(xValTensor).dataSync();
    const yPred = yPredProb.map((prob) => (prob > 0.5 ? 1 : 0));

    const metrics = calculateMetrics(yValTensor.dataSync(), yPred, yPredProb);

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
      bestModel = model;
      bestMetrics = metrics;
    }
  }

  bestModel.summary();
  console.log(`Best model metrics: ${bestMetrics}`);

  const modelInfo = await getModelInfo(bestModel);

  dbInfo.model = modelInfo;

  return [dbInfo, sensorData];
};
