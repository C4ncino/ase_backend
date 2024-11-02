export const InputConfig = {
  returnSequences: true,
  inputShape: [60, 8],
}

export const Initializers = {
  kernelInitializer: "heNormal",
  recurrentInitializer: "heNormal",
}

export const calculateBatchSize = (totalSize) => {
  const quarterSize = Math.floor(totalSize / 4);

  if (quarterSize >= 128) 
    return 128;

  let batchSize = 1;
  while (batchSize <= quarterSize) {
      batchSize *= 2;
  }
  batchSize /= 2;

  return Math.floor(batchSize);
}

export const logMetrics = (metrics) => {
  console.log(`
    Best Model Metrics:
    -------------------
    - Accuracy:     ${metrics.accuracy.toFixed(4)}
    - ROC AUC:      ${metrics.roc_auc.toFixed(4)}
    - Precision:    ${metrics.precision.toFixed(4)}
    - Recall:       ${metrics.recall.toFixed(4)}
    - F1 Score:     ${metrics.f1_score.toFixed(4)}
  `);
}
