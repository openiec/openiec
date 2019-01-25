"""
Obtain quantities correlating with thremodynamic equilibrium calculation using the pycalphad package.
"""

import matplotlib.pyplot as plt
from pycalphad import equilibrium
from pycalphad import Database, Model
import pycalphad.variables as v
import numpy as np
import math


class CoherentGibbsEnergy(object):
    """
    Equilibrium calculation for sing phase or two phases.

    Parameters
    ----------
    T: float
        Given temperature.
    db : Database
        Database containing the relevant parameters.
    comp: str
        Name of pure component.
    phasename: list
        Name of phase model to build.
    """

    def __init__(self, T, db, comps, phasename):
        self.T = T
        self.comps = comps
        self.phasename = phasename
        self.P = 101325
        self.db = db

    def eqfunc(self, x):
        """
        Calculate the phase equilibrium.
        """
        variable = x + [self.T, self.P]
        xs = [v.X(each) for each in self.comps if each != "VA"]
        xxs = [xs[i] for i in range(1, len(xs))]
        xxxs = xxs + [v.T, v.P]
        var = {xxxs[i]: variable[i] for i in range(len(variable))}
        eq_result = equilibrium(self.db, self.comps, self.phasename, var)
        return eq_result

    def phase(self, x, **kwargs):
        """
        The string name of the phase in equilibrium at the conditions.
        """
        phasearray = self.eqfunc(x).Phase.sel(P=self.P, T=self.T, **kwargs)
        return phasearray.values.flatten()

    def phasevertex(self, x, **kwargs):
        """
        The phasevertex is the index of the phase in equilibrium. 
        """
        phaseindex = []
        for each in self.phasename:
            phasevertex = (
                self.eqfunc(x)
                .vertex.where(self.eqfunc(x).Phase == each)
                .sel(P=self.P, T=self.T, **kwargs)
            )
            indexarray = phasevertex.values
            index = [value for value in indexarray.ravel() if not math.isnan(value)]
            phaseindex += index
        return phaseindex

    def Gibbsenergy(self, x, **kwargs):
        """
        Molar Gibbs energy of bulk phases.
        """
        GM = self.eqfunc(x).GM.sel(P=self.P, T=self.T, **kwargs)
        return GM.values.flatten()

    def chemicalpotential(self, x, **kwargs):
        """
        Chemical potentials of components in bulk phases.

        Parameters
        ----------
        componentname: list
            Names of components to consider in the calculation.    
        """
        componentname = [each for each in self.comps if each != "VA"]
        chemicalpotential = (
            self.eqfunc(x).MU.sel(P=self.P, T=self.T, component=componentname, **kwargs)
        ).values
        return chemicalpotential.flatten()

    def phasefraction(self, x, **kwargs):
        """
        Phase fractions of phases in equilibrium.
        """
        phaseindex = self.phasevertex(x, **kwargs)
        phasefraction = [
            (
                self.eqfunc(x)
                .NP.where(self.eqfunc(x).Phase == self.phasename[i])
                .sel(P=self.P, T=self.T, vertex=phaseindex[i], **kwargs)
            ).values
            for i in range(len(self.phasename))
        ]
        return phasefraction

    def molefraction(self, x, **kwargs):
        """
        Mole fractions of components for phases in equilibrium.

        Parameters
        ----------
        componentname: list
            Names of components to consider in the calculation.
        """
        components = [each for each in self.comps if each != "VA"]
        phaseindex = self.phasevertex(x, **kwargs)
        molefraction = [
            [
                (
                    self.eqfunc(x)
                    .X.where(self.eqfunc(x).Phase == self.phasename[i])
                    .sel(
                        P=self.P,
                        T=self.T,
                        component=ceach,
                        vertex=phaseindex[i],
                        **kwargs
                    )
                ).values
                for ceach in components
            ]
            for i in range(len(self.phasename))
        ]
        return molefraction

    def componentindex(self, x, **kwargs):
        """
        The componentindex is the index of the component in equilibrium. 
        """
        compsindex = []
        for each in self.phasename:
            componentindex = (
                self.eqfunc(x)
                .component.where(self.eqfunc(x).Phase == each)
                .sel(P=self.P, T=self.T, **kwargs)
            )
            indexarray = componentindex.values
            index = indexarray[indexarray != "nan"]
            index = set(index)
            compsindex.append(list(index))
        return compsindex

    def sitefraction(self, x, **kwargs):
        """
        Site fractions of components for phases in equilibrium.
        """
        phaseindex = self.phasevertex(x, **kwargs)
        ysdims = self.eqfunc(x).dims["internal_dof"]
        yys = [
            [
                (
                    self.eqfunc(x)
                    .Y.where(self.eqfunc(x).Phase == self.phasename[i])
                    .isel(internal_dof=index)
                    .sel(P=self.P, T=self.T, vertex=phaseindex[i], **kwargs)
                ).values
                for index in range(ysdims)
            ]
            for i in range(len(self.phasename))
        ]
        return yys

