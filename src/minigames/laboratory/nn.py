import json

import numpy as np


class Layer:
    def __init__(self, weights, biases):
        self.weights = np.array(weights, dtype=float).T
        self.biases = np.array(biases, dtype=float)

    def forward(self, x):
        return np.dot(x, self.weights) + self.biases


def relu(x):
    return np.maximum(0, x)


def softmax(x):
    x = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


class NeuralNetwork:
    def __init__(self, json_path):
        with open(json_path, "r") as f:
            data = json.load(f)

        self.hidden1 = self._load_layer(data, "hidden1")
        self.hidden2 = self._load_layer(data, "hidden2")
        self.output = self._load_layer(data, "output")

    def _load_layer(self, data, name):
        if name not in data:
            raise ValueError(f"Layer '{name}' not found")
        return Layer(data[name]["weights"], data[name]["biases"])

    def forward(self, x):
        x = np.array(x, dtype=np.float32).reshape(1, -1)
        x = relu(self.hidden1.forward(x))
        x = relu(self.hidden2.forward(x))
        x = softmax(self.output.forward(x))
        return x

    def predict(self, x):
        probs = self.forward(x)
        index = np.argmax(probs, axis=1)[0]
        return int(index)
