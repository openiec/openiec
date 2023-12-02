"""
Construct the function of calculating the melting enthalpy of the pure metal.
"""

from pycalphad import equilibrium
from pycalphad import Database, Model
# import pycalphad.variables as V
import openiec.variables as V
from sympy import lambdify, symbols, sympify, diff, Symbol
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def RenderPhas(db, comp, phasename):
    """
    Render the molar Gibbs energy and the molar enthalpy of the pure metal in the bulk phase.

    Parameters
    -----------
    db : Database
        Database containing the relevant parameters.
    comp: str
        Name of pure component.
    phasename: list
        Name of phase model to build.
    """
    model = Model(db, [comp, "VA"], phasename)
    gm = model.ast
    vars = {V.Y(phasename, 1, "VA"): 1.0, V.R: 8.31451, V.Y(phasename, 0, comp): 1.0}
    gm = gm.subs(vars)
    return {
        "gm": lambdify(V.T, gm, "numpy", dummify=True),
        "hm": lambdify(V.T, -V.T ** 2 * diff(gm / V.T, V.T), "numpy", dummify=True),
    }


def MeltingEnthalpy(db, comp, phasenames, debug=False):
    """
    Calculate the melting enthalpy of the pure metal.

    Parameters
    -----------
    db : Database
        Database containing the relevant parameters.
    comp: str
        Name of pure component.
    phasename: list
        Name of phase model to build.
    """
    alpha = RenderPhas(db, comp, phasenames[0])
    beta = RenderPhas(db, comp, phasenames[1])
    fbeta, falpha = beta["gm"], alpha["gm"]
    hbeta, halpha = beta["hm"], alpha["hm"]

    f = lambda T: fbeta(T) - falpha(T)
    x = np.linspace(298.15, 3000, 10000)
    v = f(x)

    if debug:
        plt.plot(x, v, "-", label="diff")
        plt.plot(x, v * 0.0, "--", label="zero")
        plt.plot(x, falpha(x), label="%s" % phasenames[0])
        plt.plot(x, fbeta(x), label="%s" % phasenames[1])
        plt.legend()
        plt.show()

    v = v[0:-1] * v[1:]
    index = np.where(v < 0.0)

    if len(index[0]) == 0:
        print("[Error] No melting point for the current component is found")
        return 0

    x0 = fsolve(f, x[index])

    deltaH = abs(halpha(x0) - hbeta(x0))

    return deltaH[0]
