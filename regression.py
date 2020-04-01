import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

class Exp:
    """
    class that handles exponential regression
    """
    def __init__(self, data, country, type):
        """
        data is from data.py
        country is a string containing the country name
        type is an int:
        0 => confirmed
        1 => dead
        2 => recovered
        """
        self.data = data
        self.country = country
        self.type = type
        self.types = ["confirmed", "deaths", "recovered"]
        self.get_data()
    def get_data(self):
        """
        Gathers data from given dataset
        """
        self.x = -1
        self.y = -1
        if self.type == 0:
            self.x = np.array([i for i in range(len(self.data.confirmed_dict[self.country]))])
            self.y = np.array(self.data.confirmed_dict[self.country])
        elif self.type == 1:
            self.x = np.array([i for i in range(len(self.data.death_dict[self.country]))])
            self.y = np.array(self.data.death_dict[self.country])
        elif self.type == 2:
            self.x = np.array([i for i in range(len(self.data.recover_dict[self.country]))])
            self.y = np.array(self.data.recover_dict[self.country])
    def transform_parameters(self):
        """
        takes log of y, and log of 1 when y==0
        """
        ys = []
        for v in self.y:
            if v <= 0:
                ys.append(np.log(1))
            else:
                ys.append(np.log(v))
        self.y_trans = ys
    def fit(self):
        """
        fits the data and makes prediction
        """
        self.f = np.polyfit(self.x,self.y_trans, 1, w=np.sqrt(self.y))
        self.y_pred = np.array([np.exp(self.f[1]) * np.exp(self.f[0] * i) for i in self.x])
    def score(self):
        """
        gets r^2 value
        """
        self.r2 = r2_score(self.y, self.y_pred)
    def get_form(self):
        """
        gets a string form of the equation for the given model
        """
        self.form = str(np.exp(self.f[1])) + "*" + str(np.exp(self.f[0])) + "x"
    def get_rmse(self):
        """
        gets the rmse value for the predicted function
        """
        self.rmse = np.sqrt(mean_squared_error(self.y, self.y_pred))
    def exp_reg(self):
        """
        func takes any parameter and predicts the output
        """
        self.transform_parameters()
        self.fit()
        self.score()
        self.get_form()
        self.get_rmse()
        self.func = lambda x: np.exp(self.f[1]) * np.exp(self.f[0]*x)
    def show(self):
        """
        shows the prediction function graphed against the original function
        labels are r^2
        """
        plt.scatter(self.x, self.y)
        plt.title("{} vs. time".format(self.types[self.type]))
        plt.xlabel("days since 1/22/2022")
        plt.ylabel("# {}".format(self.types[self.type]))
        plt.plot(self.x, self.y_pred, label="r^2: {:.2f}".format(self.r2))
        plt.legend(loc='upper left')
        plt.show()
    def predict(self, val):
        """
        predicts for any given value
        """
        return self.func(val)

class Poly:
    def __init__(self, data, country, type):
        """
        data is from data.py
        country is a string containing the country name
        type is an int:
        0 => confirmed
        1 => dead
        2 => recovered
        """
        self.data = data
        self.country = country
        self.type = type
        self.types = ["confirmed", "deaths", "recovered"]
        self.get_data()
        self.transform_data()
    def get_data(self):
        self.x = -1
        self.y = -1
        if self.type == 0:
            self.x = np.array([i for i in range(len(self.data.confirmed_dict[self.country]))])
            self.y = np.array(self.data.confirmed_dict[self.country])
        elif self.type == 1:
            self.x = np.array([i for i in range(len(self.data.death_dict[self.country]))])
            self.y = np.array(self.data.death_dict[self.country])
        elif self.type == 2:
            self.x = np.array([i for i in range(len(self.data.recover_dict[self.country]))])
            self.y = np.array(self.data.recover_dict[self.country])
    def transform_data(self):
        self.x_change = np.array(self.x).reshape(-1, 1)
        self.y_change = np.array(self.y).reshape(-1, 1)
    def model_fit(self, d):
        self.poly_features = PolynomialFeatures(degree=d)
        self.x_poly = self.poly_features.fit(self.x_change)
        self.model = LinearRegression()
        self.model.fit(self.x_poly, self.y_change)
        self.y_pred = self.model.predict(self.x_poly)
        self.r2 = r2_score(self.y_change, self.y_pred)
        self.rmse = np.sqrt(mean_squared_error(self.y_change, self.y_pred))
    def poly_reg(self):
        best_r2 = 0
        best_d = 0
        self.best_degrees = []
        for i in range(50):
            self.model_fit(i)
            if self.r2 > best_r2:
                best_r2 = new_r2
                best_d = i
                self.best_degrees.append(i)
        self.best_degree = self.best_degrees[-1]
        self.model_fit(self.best_degree)
    def show(self):
        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.y_pred)
        plt.show()
