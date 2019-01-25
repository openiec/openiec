"""
Construct partial excess Gibbs energy expressions of the bulk phase and the interface surrouded the two adjacent phases.
"""

from pycalphad import equilibrium
from pycalphad import Database, Model
import pycalphad.variables as V
from sympy import lambdify, symbols, sympify, diff
from functools import reduce


class SubModel(Model):
    """
    Render the excess Gibbs energy from the thermodynamic database.
    """

    contributions = [("xsmix", "excess_mixing_energy")]


class SolutionGibbsEnergy(object):
    """
    Construct the excess Gibbs energy expression of the builk phase.

    Parameters
    -----------
    T: float
        Given temperature.
    db : Database
        Database containing the relevant parameters.
    comp: str
        Name of pure component.
    phasename: str
        One of two bulk phases.
    """

    def __init__(self, T, db, comps, phasename):
        vars = {V.Y(phasename, 1, "VA"): 1.0, V.R: 8.31451, V.T: T}

        xs = [V.Y(phasename, 0, each) for each in comps if each != "VA"]
        vars_xs = [(xs[0], 1.0 - sum([xs[i] for i in range(1, len(xs))]))]
        self.xxs = [xs[i] for i in range(1, len(xs))]

        model = SubModel(db, comps, phasename)
        sympy_exgm = model.ast
        exgm = sympy_exgm.subs(vars)

        dgmdy = [diff(exgm, x) for x in xs]

        sumpartial = reduce(
            lambda x, y: x + y, [xs[i] * dgmdy[i] for i in range(len(xs))]
        )
        pexgm = [exgm + dgmdy[i] - sumpartial for i in range(len(xs))]

        exgm = exgm.subs(vars_xs)
        pexgm = [each.subs(vars_xs) for each in pexgm]

        self.lam_exgm = lambdify(self.xxs, exgm, "numpy", dummify=True)
        self.lam_pexgm = [
            lambdify(self.xxs, each, "numpy", dummify=True) for each in pexgm
        ]


class InterfacialGibbsEnergy(object):
    """
    Construct the excess Gibbs energy expression of the interface.

    Parameters
    -----------
    T: float
        Given temperature.
    db : Database
        Database containing the relevant parameters.
    comp: str
        Name of pure component.
    phasename: list
        Two phases in the interface
    """

    def __init__(self, T, db, comps, phasename):
        vars1 = {V.Y(phasename[0], 1, "VA"): 1.0, V.R: 8.31451, V.T: T}

        xs1 = [V.Y(phasename[0], 0, each) for each in comps if each != "VA"]

        model1 = SubModel(db, comps, phasename[0])
        sympy_exgm1 = model1.ast
        exgm1 = sympy_exgm1.subs(vars1)

        vars2 = {V.Y(phasename[1], 1, "VA"): 1.0, V.R: 8.31451, V.T: T}

        xs2 = [V.Y(phasename[1], 0, each) for each in comps if each != "VA"]

        model2 = SubModel(db, comps, phasename[1])
        sympy_exgm2 = model2.ast
        exgm2 = sympy_exgm2.subs(vars2)

        vars_xs = [(xs1[i], xs2[i]) for i in range(len(xs1))]
        xs = [each for each in xs2]
        vars_xxs = [(xs[0], 1.0 - sum([xs[i] for i in range(1, len(xs))]))]
        self.xxs = [xs[i] for i in range(1, len(xs))]

        sympy_exgm = 0.5 * (exgm1 + exgm2)
        exgm = sympy_exgm.subs(vars_xs)

        dgmdy = [diff(exgm, x) for x in xs]

        sumpartial = reduce(
            lambda x, y: x + y, [xs[i] * dgmdy[i] for i in range(len(xs))]
        )
        pexgm = [exgm + dgmdy[i] - sumpartial for i in range(len(xs))]

        exgm = exgm.subs(vars_xxs)
        pexgm = [each.subs(vars_xxs) for each in pexgm]
        self.lam_exgm = lambdify(self.xxs, exgm, "numpy")
        self.lam_pexgm = [
            lambdify(self.xxs, each, "numpy", dummify=True) for each in pexgm
        ]

