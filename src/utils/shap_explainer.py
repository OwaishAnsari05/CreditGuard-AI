import shap
import pandas as pd


class SHAPExplainer:

    def __init__(self, model, preprocessor, feature_names):

        self.model = model
        self.preprocessor = preprocessor
        self.feature_names = feature_names

        self.explainer = shap.TreeExplainer(self.model)

    def explain(self, input_df):

        # Transform input

        X = self.preprocessor.transform(input_df)

        # SHAP values

        shap_values = self.explainer.shap_values(X)

        # Binary classifier compatibility
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        shap_row = shap_values[0]

        # Feature Importance

        importance = pd.DataFrame({

            "Feature": self.feature_names,
            "SHAP": shap_row

        })

        importance["Impact"] = importance["SHAP"].abs()

        importance = importance.sort_values(
            by="Impact",
            ascending=False
        )

        return importance.head(5)