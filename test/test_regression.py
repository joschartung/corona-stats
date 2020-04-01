import numpy as np
import matplotlib.pyplot as plt
import data as d
import regression

def test_exp():
    reg = regression.Exp(d, "China", 0)
    reg.exp_reg()
    print(reg.func(70))
    reg.show()
def test_reg():
    reg = regression.Poly(d, "US", 0)
    reg.poly_reg()
    reg.show()
