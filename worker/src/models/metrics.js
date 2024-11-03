export const flatResult = async (result) => {
  let predictions;

  if (Array.isArray(result)) {
    const predictionsArray = await Promise.all(
      result.map((tensor) => tensor.dataSync())
    );

    const flattened = predictionsArray.flat();

    predictions = new Float32Array(flattened.length);

    let offset = 0;
    predictionsArray.forEach((arr) => {
      predictions.set(arr, offset);
      offset += arr.length;
    });
  } else {
    predictions = await result.data();
  }

  return predictions;
};
const calculateRocAuc = (y_true, y_pred_prob) => {
  const data = y_true.map((value, index) => ({
    label: value,
    prob: y_pred_prob[index],
  }));
  data.sort((a, b) => b.prob - a.prob);

  let tpr = 0;
  let fpr = 0;

  const totalPositives = data.filter((d) => d.label === 1).length;
  const totalNegatives = data.length - totalPositives;

  return (
    data.reduce((auc, curr) => {
      if (curr.label === 1) {
        tpr++;
      } else {
        fpr++;
        auc += tpr / totalPositives;
      }
      return auc;
    }, 0) / totalNegatives
  );
};

export const calculateMetrics = (y_true, y_pred) => {
  const yTrue = Array.from(y_true);
  const yPred = Array.from(y_pred);

  const tp = yTrue.reduce(
    (acc, val, i) => acc + (val === 1 && yPred[i] === 1 ? 1 : 0),
    0
  );
  const fp = yTrue.reduce(
    (acc, val, i) => acc + (val === 0 && yPred[i] === 1 ? 1 : 0),
    0
  );
  const fn = yTrue.reduce(
    (acc, val, i) => acc + (val === 1 && yPred[i] === 0 ? 1 : 0),
    0
  );

  const accuracy = (tp + (yTrue.length - tp - fp - fn)) / yTrue.length;
  const precision = tp / (tp + fp) || 0;
  const recall = tp / (tp + fn) || 0;
  const f1_score = (2 * (precision * recall)) / (precision + recall) || 0;

  const roc_auc = calculateRocAuc(yTrue, yPred);

  return {
    accuracy,
    precision,
    recall,
    f1_score,
    roc_auc,
  };
};

export const hasBetterMetrics = (current_metrics, best_metrics) => {
  const metrics = ["roc_auc", "f1_score", "precision", "recall", "accuracy"];

  for (const metric of metrics) {
    if (current_metrics[metric] > best_metrics[metric]) {
      return true;
    } else if (current_metrics[metric] < best_metrics[metric]) {
      break;
    }
  }

  return false;
};

export const earlyStoppingCallback = {
  monitor: "val_loss", // Métrica a monitorear
  patience: 5, // Épocas sin mejora antes de detenerse
  minDelta: 0.001, // Mínima mejora requerida
  bestValMetric: Infinity,
  epochsWithoutImprovement: 0,

  onEpochEnd: async function (epoch, logs) {
    const currentValMetric = logs["val_loss"];
    console.log(`Epoch ${epoch + 1} - "val_loss": ${currentValMetric}`);

    console.log(
      this.minDelta,
      this.bestValMetric,
      this.epochsWithoutImprovement
    );
    console.log(this.monitor, this.patience);

    if (currentValMetric < this.bestValMetric - this.minDelta) {
      this.bestValMetric = currentValMetric;
      this.epochsWithoutImprovement = 0;
    } else {
      this.epochsWithoutImprovement += 1;
    }

    if (this.epochsWithoutImprovement >= this.patience) {
      console.log(`Early stopping triggered on epoch ${epoch + 1}`);
      this.model.stopTraining = true;
    }
  },
};

export const createEarlyStoppingCallback = (model) => {
  let bestValLoss = Infinity;
  let epochsWithoutImprovement = 0;
  const patience = 5; // Épocas sin mejora antes de detenerse
  const minDelta = 0.001; // Mínima mejora requerida

  return {
    onEpochEnd: (epoch, logs) => {
      const currentValLoss = logs.val_loss;
      console.log(`Epoch ${epoch + 1} - val_loss: ${currentValLoss}`);
      console.log(epochsWithoutImprovement);

      if (currentValLoss < bestValLoss - minDelta) {
        bestValLoss = currentValLoss;
        epochsWithoutImprovement = 0; // Reiniciar contador
      } else {
        epochsWithoutImprovement += 1; // Incrementar si no hay mejora
      }

      if (epochsWithoutImprovement >= patience) {
        console.log(`Early stopping triggered on epoch ${epoch + 1}`);
        model.stopTraining = true; // Detener entrenamiento
      }
    },
  };
};
