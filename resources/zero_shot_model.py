import logging
logging.basicConfig(level=logging.INFO)

from transformers import pipeline


class ZeroShotClassifier:
    def __init__(self, model_name):
        self.classifier = pipeline("zero-shot-classification", model=model_name)

    def predict(self, text, candidate_labels):
        return self.classifier(text, candidate_labels)
