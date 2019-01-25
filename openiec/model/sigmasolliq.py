"""
Contruct the partial interfacial energies for different components on the coherent interface and the object function to resolving the interfacial equilibrium condition.
"""

from openiec.utils.makemultigrid import makemultigrid
from scipy.optimize import minimize
from math import fabs
import numpy as np
from functools import reduce


class SigmaPureMetal(object):
    """
    Contruct the solid/liquid interfacial energies of pure components.

    Parameters
    -----------
    deltaH: float
        The standard molar entholpy of melting of the pure component.
    purevm: float
        The characteristic molar volume of pure component.
    """

    def __init__(self, deltaH, purevm):
        self.deltaH = deltaH
        self.purevm = purevm
        self.R = 8.31451
        self.NAv = 6.02 * 10.0 ** 23

    def infenergy(self, T):
        sigma = (self.deltaH + 0.5 * self.R * T * np.log(2)) / (
            2.0 * self.purevm ** (2.0 / 3.0) * self.NAv ** (1.0 / 3.0)
        )
        return sigma


class SigmaSolidLiquidInterface(object):
    """
    Contruct the interfacial energy of the solid/liquid interface and their partial quantaties.

    Parameters
    -----------        
    T: float
        Given temperature for calculating interfacial energy
    xS: list
        Mole fractions of components in solid phase at two-phase equilibrium
    xL: list
        Mole fractions of components in loquid phase at two-phase equilibrium
    omega: list
        Molar interfacial areas of components
    sigma0: 
        Solid/liquid interfacial energies of pure components
    excessgmI: list
        Partial molar excess Gibbs energies of components in the solid/liquid interfacial region
    excessgmS: list
        Partial molar excess Gibbs energies of components in solid phase
    excessgmL: list
        Partial molar excess Gibbs energies of components in liquid phase
    """

    def __init__(self, T, xS, xL, omega, sigma0, excessgmI, excessgmS, excessgmL):
        self.T = T
        self.xS = xS
        self.xL = xL
        self.omega = omega
        self.sigma0 = sigma0
        self.excessgmI = excessgmI
        self.excessgmS = excessgmS
        self.excessgmL = excessgmL
        self.R = 8.31451
        self.NAv = 6.02 * 10.0 ** 23

    def infenergy(self, x):
        """
        Compute solid/liquid partial interfacial energies of various components.
        
        Parameters
        ----------
        x: list
            Interfacial composition.        
        """
        xx = [each for each in x]
        xx.insert(0, 1 - sum(x))
        sigma = [
            self.sigma0[i]
            + (
                self.R
                * self.T
                * np.log(xx[i] * ((self.xS[i] * self.xL[i]) ** (-1.0 / 2.0)))
            )
            / self.omega[i]
            + (
                2.0 * self.excessgmI[i](*x)
                - self.excessgmS[i](*x)
                - self.excessgmL[i](*x)
            )
            / (2.0 * self.omega[i])
            for i in range(len(x) + 1)
        ]
        return sigma

    def objective(self, x):
        """
        Compute the absolute value of the differences between the partial interfacial energy.
        
        Parameters
        ----------
        x: list
            Interfacial composition.
        """
        v = 0.0
        s = self.infenergy(x)
        for i in range(len(s) - 1):
            for j in range(i + 1, len(s)):
                v += fabs(s[i] - s[j])
        return v
