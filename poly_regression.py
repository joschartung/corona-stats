import numpy as np
import matplotlib.pyplot as plt
import data as d
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

def transform_data(x,y):
    """
    x and y must be 1d numpy arrays
    """
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]
    return x, y

def poly_regression(x, y, d=2):
    """
    x and y must have been transformed using transform_data
    d must be an integer representing the degree of the polynomial
    returns a dictionary with the model, x_poly, y_poly_predicted, r2, rmse, and degree of the model
    """
    poly_features = PolynomialFeatures(degree=d)
    x_poly = poly_features.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly)
    rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
    r2 = r2_score(y,y_poly_pred)
    vals = {"model":model, "x_poly":x_poly,"y_poly_pred":y_poly_pred, "r2":r2, "rmse":rmse, "degree": d}
    return vals

def find_best(x,y):
    """
    finds the best possible model for given x,y data that has been transformed already
    """
    best_r2 = 0
    best_degree = 0
    models = []
    best_index = 0
    for i in range(50):
        results = poly_regression(x, y, i)
        new_r2 = results["r2"]
        if new_r2 > best_r2:
            best_r2 = new_r2
            best_degree = results["degree"]
            best_index = i
        models.append(results)
    return models[best_index]

def nonlinear_regression(country, type):
    """
    country is a string for any given country
    type is either confirmed, dead, or recovered
    """
    if type == "confirmed":
        x = np.array([i for i in range(len(d.confirmed_dict[country]))])
        y = np.array(d.confirmed_dict[country])
    elif type == "dead":
        x = np.array([i for i in range(len(d.death_dict[country]))])
        y = np.array(d.death_dict[country])
    elif type == "recovered":
        x = np.array([i for i in range(len(d.recover_dict[country]))])
        y = np.array(d.recover_dict[country])
    x,y = transform_data(x,y)
    best = find_best(x,y)
    return best
