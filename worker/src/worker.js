"use strict";
import celery from "celery-node";
import { trainModels } from "./tasks/train-small.js";
import { trainLargeModel } from "./tasks/train-large.js";
import "@tensorflow/tfjs-node";

const celeryWorker = celery.createWorker("redis://redis", "redis://redis");

celeryWorker.register("train_models", trainModels);
celeryWorker.register("train_large_model", trainLargeModel);

celeryWorker.start();


