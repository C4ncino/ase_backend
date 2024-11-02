import { getModel, SMALL_MODEL_POOL } from "../models/small-models.js";
import { calculateMetrics, hasBetterMetrics, createEarlyStoppingCallback } from "../models/metrics.js";
import { getModelInfo } from "../models/save-model.js"
import {log, tensor} from "@tensorflow/tfjs";
import {minimizeModel} from "../models/minimizer.js"
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
      // verbose: 0,
      callbacks: [callBack]
    });

    const minModel = minimizeModel(model);

    console.log(model.layers[0].getWeights()[0].dataSync()[0])
    console.log(minModel.layers[0].getWeights()[0].dataSync()[0])
    

    const yPredMinProb = minModel.predict(xValTensor).dataSync();
    const yPredMin = yPredMinProb.map((prob) => (prob > 0.5 ? 1 : 0));

    const yPredProb = model.predict(xValTensor).dataSync();
    const yPred = yPredProb.map((prob) => (prob > 0.5 ? 1 : 0));

    const metrics = calculateMetrics(yValTensor.dataSync(), yPred, yPredProb);
    const minMetrics = calculateMetrics(yValTensor.dataSync(), yPredMin, yPredMinProb);


    logMetrics(metrics);
    logMetrics(minMetrics);

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

  bestModel = minimizeModel(bestModel, 16, 0.01);

  const modelInfo = await getModelInfo(bestModel);

  dbInfo.model = modelInfo;

  return [dbInfo, sensorData];
};
