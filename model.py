import numpy as np
from sklearn.linear_model import LinearRegression

def train_models(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model, "Linear Regression"


def predict_future(model, last_day, days):
    future_X = np.arange(last_day+1, last_day+days+1).reshape(-1,1)
    return model.predict(future_X)