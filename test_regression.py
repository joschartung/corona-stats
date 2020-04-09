import numpy as np
import matplotlib.pyplot as plt
import dataset as d
import regression

def test_exp():
    data = d.Data()
    reg = regression.Exp(data, "US", 0)
    reg.exp_reg()
    print(reg.func(70))
    reg.show()
def test_poly():
    data = d.Data()
    reg = regression.Poly(data, "US", 0)
    reg.poly_reg()
    reg.show()
def test_log():
    data = d.Data()
    reg = regression.Log(data, "US", 0)
    print(reg.pred(78))
    reg.show()

test_log()
