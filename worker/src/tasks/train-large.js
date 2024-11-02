import {get_large_model} from "../models/large-models.js"
import {tensor} from "@tensorflow/tfjs";
import { getModelInfo } from "../models/save-model.js"
import {minimizeModel} from "../models/minimizer.js"
import { calculateBatchSize } from "../models/utils.js";

export const trainLargeModel = async (trainingData, nClases, userId) => {
    const { xTrain, xVal, yTrain, yVal } = trainingData;

    console.log(xTrain.length, xVal.length, yTrain.length, yVal.length);

    const xTensor = tensor(xTrain);
    const yTensor = tensor(yTrain);
    const xValTensor = tensor(xVal);
    const yValTensor = tensor(yVal);

    const batchSize = calculateBatchSize(xTrain.length);

    let model = get_large_model("L1", nClases);

    await model.fit(xTensor, yTensor, {
        epochs: 50,
        batchSize: batchSize,
        validationData: [xValTensor, yValTensor],
        // verbose: 0,
    });

    model.summary();

    model = minimizeModel(model, 16, 0.01);

    const modelInfo = await getModelInfo(model);

    return [modelInfo, userId]
}