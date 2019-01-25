"""
Construct the molar volume CALPHAD model.
"""

import numpy as np
import sympy as sy
import pycalphad.variables as V
from pycalphad import Database, Model
from sympy import lambdify, symbols, sympify, diff
import itertools
from functools import reduce


class MolarVolume(object):
    """
    Construct molar volumes of bulk phases.

    Parameters
    -----------
    db : Database
        Database containing the relevant parameters.
    comps : list
        Names of components to consider in the calculation.
    phasename : str
        Names of the phase to consider in the calculation.    
    purevm: list 
        The molar volume of the components.
    vm: a sympy expression
        The molar volume of the bulk phase.
    """

    def __init__(self, db, phasename, comps, purevm, intervm=[]):
        self.xs = [V.X(each) for each in comps if each != "VA"]
        self.vars_xs = [
            (self.xs[0], 1.0 - sum([self.xs[i] for i in range(1, len(self.xs))]))
        ]
        self.xxs = [self.xs[i] for i in range(1, len(self.xs))]
        self.vm = reduce(
            lambda x, y: x + y, [x * sympify(v) for x, v in zip(self.xs, purevm)]
        ).subs({"T": V.T})


def InterficialMolarVolume(alphavm, betavm):
    """
    Construct the partial molar volume of the interface.

    Parameters
    -----------
    alphavm: a sympy expression
        The molar volume of a bulk phase.
    betavm: a sympy expression
        The molar volume of another bulk phase.
    vm: a sympy expression
        The molar volume of the interfacial layer.
    vmis: list
        The partial molar volumes of components in the interface.
    """
    xs = alphavm.xs
    vm = 0.5 * (alphavm.vm + betavm.vm)
    dvmdxs = [diff(vm, x) for x in xs]

    sumvmi = reduce(lambda x, y: x + y, [x * dvmdx for x, dvmdx in zip(xs, dvmdxs)])

    vmis = [vm + dvmdx - sumvmi for dvmdx in dvmdxs]

    return [lambdify((alphavm.xxs, V.T), vmi, "numpy", dummify=True) for vmi in vmis]


if __name__ == "__main__":
    db = Database("NiAl.tdb")
    alphavm = MolarVolume(db, "FCC_A1", ["Ni", "Al"], ["1.0*T", "2.0*T"])
    betavm = MolarVolume(db, "LIQUID", ["Ni", "Al"], ["1.0*T", "2.0*T"])
    vm = InterficialMolarVolume(alphavm, betavm)

    print(vm[0]([0.9], 100.0), vm[1]([0.9], 100.0))

