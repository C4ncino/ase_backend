import { tensor } from "@tensorflow/tfjs";


export const minimizeModel = (model, bitDepth = 8, threshold = 0.0075) => {
    const scaleFactor = Math.pow(2, bitDepth - 1) - 1;
  try {
    
      for (const layer of model.layers) {
          const weights = layer.getWeights();
          const prunedWeights = weights.map(weight => {
              const data = weight.dataSync();
              const prunedData = new Float32Array(data.length);

              for (let i = 0; i < data.length; i++) {  
                //* Prune
                prunedData[i] = Math.abs(data[i]) < threshold? 0 : data[i];

  
                //? Quantize
                // console.log(`Quantizing: ${data[i].toPrecision(30)}`);
                
                // prunedData[i] = Math.round(data[i] * scaleFactor) / scaleFactor;

                // console.log(`Quantized: ${prunedData[i].toPrecision(30)}`);
                
              }
              return tensor(prunedData, weight.shape, weight.dtype);
          });
          layer.setWeights(prunedWeights);
      }
  } catch (error) {
    console.error(error);
  }

    return model;
}