import fs from "node:fs";
import os from "node:os";
import path from "node:path";

export const getModelInfo = async (model) => {
  const modelInfo = {
    json: {},
    weights: {},
  };

  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "model"));

  await model.save("file://" + tmpDir);

  const modelJsonPath = path.join(tmpDir, "model.json");

  const modelJsonContent = fs.readFileSync(modelJsonPath, {
    encoding: "utf-8",
  });

  modelInfo.json = JSON.parse(modelJsonContent);

  const weightsManifest = modelInfo.json["weightsManifest"];

  for (const weights of weightsManifest)
    for (const weightFile of weights["paths"]) {
      const weightPath = path.join(tmpDir, weightFile);

      const weightContent = fs.readFileSync(weightPath, { encoding: null });

      modelInfo.weights[weightFile] = weightContent.toString("base64");
    }

  // fs.rmSync(tmpDir, { recursive: true });

  return modelInfo;
};
