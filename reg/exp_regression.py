import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error
import data as d

def get_data(country, type):
    if type == "confirmed":
        x = np.array([i for i in range(len(d.confirmed_dict[country]))])
        y = np.array(d.confirmed_dict[country])
    elif type == "dead":
        x = np.array([i for i in range(len(d.death_dict[country]))])
        y = np.array(d.death_dict[country])
    elif type == "recovered":
        x = np.array([i for i in range(len(d.recover_dict[country]))])
        y = np.array(d.recover_dict[country])
    else:
        return 0,0
    return x,y

def transform_y(y):
    ys = []
    for v in y:
        if v <= 0:
            ys.append(np.log(1))
        else:
            ys.append(np.log(v))
    return(ys)

def fit(x,y, log_y):
    f = np.polyfit(x, log_y, 1, w=np.sqrt(y))
    y_pred = np.array([np.exp(f[1]) * np.exp(f[0]*i) for i in x])
    return f, y_pred

def score(y, y_pred):
    r2 = r2_score(y, y_pred)
    return r2

def get_form(f):
    form = str(np.exp(f[1])) + "*" + str(np.exp(f[0])) + "x"
    return form

def exp_reg(country, type):
    x,y = get_data(country,type)
    log_y = transform_y(y)
    f, y_pred = fit(x,y, log_y)
    r2 = score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    form_str = get_form(f)
    reg_dict = {"log y":log_y, "y predicted":y_pred, "r2":r2, "form":form_str, "rmse":rmse}
    return reg_dict
