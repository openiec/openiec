import pycalphad.variables as v
from sympy import lambdify, symbols, sympify, diff

def X(x):
    return sympify(v.X(x))

def Y(phase_name, phase_index, component_name):
    return sympify("%s%d%s" % (phase_name, phase_index, component_name))

T = sympify(v.T)
R = sympify(v.R)
P = sympify(v.P)