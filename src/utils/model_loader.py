import json
import joblib


class ModelLoader:

    def __init__(self):

        self.model = None
        self.preprocessor = None
        self.threshold = None
        self.feature_names = None

    def load(self):

        print("Loading LightGBM Model...")

        self.model = joblib.load("models/lightgbm_model.pkl")

        print("✓ Model Loaded")

        self.preprocessor = joblib.load("models/preprocessor.pkl")

        print("✓ Preprocessor Loaded")

        self.threshold = joblib.load("models/threshold.pkl")

        print("✓ Threshold Loaded")

        with open("models/feature_names.json", "r") as f:

            self.feature_names = json.load(f)

        print("✓ Feature Names Loaded")

        print("\nEverything Loaded Successfully!")

        return (
            self.model,
            self.preprocessor,
            self.threshold,
            self.feature_names
        )