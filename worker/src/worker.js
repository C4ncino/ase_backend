"use strict";
import celery from "celery-node";
import "@tensorflow/tfjs-node";
import {ready} from "@tensorflow/tfjs";
import { trainModels } from "./tasks/train-small.js";
import { trainLargeModel } from "./tasks/train-large.js";

const start = async () => {
    await ready();
}

start();

const celeryWorker = celery.createWorker("redis://redis", "redis://redis");

celeryWorker.register("train_models", trainModels);
celeryWorker.register("train_large_model", trainLargeModel);

celeryWorker.start();


