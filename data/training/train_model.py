import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


class DurationModel:

    def __init__(self):
        self.model = LinearRegression()

    def train(self, csv_path):
        # Load dataset
        df = pd.read_csv(csv_path)

        # Features (X)
        X = df[[
            "word_count",
            "has_qmark",
            "has_exclaim",
            "has_ellipsis"
        ]]

        # Target (y)
        y = df["duration"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        self.model.fit(X_train, y_train)

        # Predict
        predictions = self.model.predict(X_test)

        # Evaluate
        error = mean_absolute_error(y_test, predictions)

        print("Model trained!")
        print("Mean Absolute Error:", round(error, 3))

    def predict(self, features):
        df = pd.DataFrame([features], columns=[
            "word_count",
            "has_qmark",
            "has_exclaim",
            "has_ellipsis"
        ])
        return self.model.predict(df)[0]