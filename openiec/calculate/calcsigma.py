"""According to given conditions and input parameters, calculate corresponding interfacial energies.
"""

from openiec.model.sigmacoint import SigmaCoherentInterface
from openiec.property.coherentenergy import CoherentGibbsEnergy
from openiec.model.sigmasolliq import SigmaPureMetal, SigmaSolidLiquidInterface
from openiec.property.solliqenergy import SolutionGibbsEnergy, InterfacialGibbsEnergy
from openiec.property.meltingenthalpy import MeltingEnthalpy
from openiec.property.molarinfarea import MolarInterfacialArea
from openiec.property.molarvolume import MolarVolume, InterficialMolarVolume
from openiec.calculate.minimize import SearchEquilibrium, ComputeEquilibrium
from openiec.utils.decorafunc import wraptem
from pycalphad import equilibrium
from pycalphad import Database, Model
import pycalphad.variables as v
import numpy as np
from xarray import Dataset


def SigmaPure(
    T, purevm, db=None, comp=None, phasenames=[], meltingenthalpy=None, debug=False
):
    """Calculate the solid/liquid interfacial energy of the pure metal.

    Parameters
    -----------
    T: float
        Given temperature.
    db : Database
        Database containing the relevant parameters.
    comp: str
        Name of pure component.
    phasenames : list
        Names of phase model to build.    
    meltingenthalpy: float
        The standard molar enthalpy of melting of the pure component.
    purevm: float
        The characteristic molar volume of pure component.

    Returns:   
    -----------
    Component：str
        Given component.
    Temperature: float
        Given temperature.
    Melting_Enthalpy: float
        The melting enthalpy of the pure component.
    Interfacial_Energy: float
        The interfacial energy of the pure component.

    Return type: xarray Dataset
    """
    if not meltingenthalpy:
        meltingenthalpy = MeltingEnthalpy(db, comp, phasenames, debug)
        print("Calculated melting enthalpy of %s: " % comp, meltingenthalpy)
    model = SigmaPureMetal(meltingenthalpy, purevm)
    sigma = model.infenergy(T)
    print("Calculated solid/liquid interfacial energy of %s: " %
          comp, sigma, "\n")

    res = Dataset(
        {
            "Component": comp,
            "Temperature": T,
            "Melting_Enthalpy": meltingenthalpy,
            "Interfacial_Energy": sigma,
        }
    )

    return res


def SigmaSolLiq(
    T, x0, db, comps, phasenames, purevms, intervms=[], omega=[], meltingenthalpy=[], sigma0=[], xeq=[], limit=[0, 1.0], dx=0.01, debug=False
):
    """
    Calculate the solid/liquid interfacial energy in alloys.

    Parameters
    -----------
    T: float
        Given temperature.
    x0: list
        Initial alloy composition.
    db : Database
        Database containing the relevant parameters.
    comps : list
        Names of components to consider in the calculation.
    phasenames : list
        Names of phase model to build.    
    purevms: list 
        The molar volume of the components.
        example:
            comps = ["NI", "AL"] 
            phasenames = ["FCC_A1", "LIQUID"]
            purevms = [["1.0*T", "2.0*T"], ["3.0*T", "4.0*T"]]
            where "1.0*T" and "2.0*T" are molar volumes of components Ni and Al in FCC_A1 phase, while "3.0*T" and "4.0*T" are molar volumes of components Ni and Al in LIQUID phase.
    omega: list
        The molar interfacial areas of components.
    meltingenthalpy: list
        The stardard melting enthalpies of pure componnets.
    sigma0: list
        Interfacial energies of pure metal.
    xeq: list
        Two-phase equilibrium composition.
    limit: list
        The limit of composition for searching interfacial composition in equilibrium.
    dx: float
        The step of composition for searching interfacial composition in equilibrium.

    Returns:   
    -----------
    Components: list of str
        Given components.
    Temperature: float
        Given temperature.
    Initial_Alloy_Composition: list
        Given initial alloy composition.
    Interfacial_Composition: list
        Interfacial composition of the grid minimization.
    Partial_Interfacial_Energies: list
        Partial interfacial energies of components.
    Interfacial_Energy: float    
        Requested interfacial energies.

    Return type: xarray Dataset
    """

    phasevm = [MolarVolume(db, phasenames[i], comps, purevms[i])
               for i in range(2)]
    _vmis = InterficialMolarVolume(*phasevm)

    """Decorate the _vmis to release the constains on temperature"""
    vmis = [each.decfunc() for each in [wraptem(T, f) for f in _vmis]]

    """Calculation for the solid/liquid interfacial energies of pure components"""
    if not omega:
        omega = [
            MolarInterfacialArea(vmis[i](x0))
            for i in range(len(comps))
            if comps[i] != "VA"
        ]

    if len(sigma0)==0 and len(meltingenthalpy)==0:
        sigma0 = [
            float(
                SigmaPure(
                    T, vmis[i](x0), db, comps[i], phasenames, debug=debug
                ).Interfacial_Energy.values
            )
            for i in range(len(comps))
            if comps[i] != "VA"
        ]

    if len(sigma0)==0 and len(meltingenthalpy)!=0:
        sigma0 = [
            float(
                SigmaPure(
                    T, vmis[i](
                        x0), db, comps[i], phasenames, meltingenthalpy[i], debug=debug
                ).Interfacial_Energy.values
            )
            for i in range(len(comps))
            if comps[i] != "VA"
        ]

    """Two-phase equilibirium composition"""
    if not xeq:
        _modeleq = CoherentGibbsEnergy(T, db, comps, phasenames)
        xeq = _modeleq.molefraction(x0)

    """Partial excess Gibbs energy in the interface """
    _modelinterface = InterfacialGibbsEnergy(T, db, comps, phasenames)
    interfacialpexgm = _modelinterface.lam_pexgm

    """Partial excess Gibbs energies in two bulk phases """
    _modelphase = [
        SolutionGibbsEnergy(T, db, comps, phasenames[i]) for i in range(len(phasenames))
    ]
    phasepexgm = [each.lam_pexgm for each in _modelphase]

    """Call the module of solid/liquid interfacial energy calculation"""
    Model = SigmaSolidLiquidInterface(
        T, xeq[0], xeq[1], omega, sigma0, interfacialpexgm, phasepexgm[0], phasepexgm[1]
    )

    components = [each for each in comps if each != "VA"]
    cum = int(len(components) - 1)
    print(
        "\n******************************************************************************\nOpenIEC is looking for interfacial equilibirium coposition.\nFor more information visit https://github.com/openiec/openiec."
    )
    x_s = SearchEquilibrium(Model.objective, [limit] * cum, [dx] * cum)
    x_c = ComputeEquilibrium(Model.objective, x_s["x"])
    print(
        "******************************************************************************\n\n"
    )
    sigma = Model.infenergy(x_c)

    xx0 = [1.0 - sum(x0)] + x0
    xx_c = [1.0 - sum(list(x_c))] + list(x_c)
    sigmapartial = list(np.array(sigma).flatten())
    sigmaavg = np.average([each for each in sigma])

    res = Dataset(
        {
            "Components": components,
            "Temperature": T,
            "Initial_Alloy_Composition": ("Components", xx0),
            "Interfacial_Composition": ("Components", xx_c),
            "Partial_Interfacial_Energy": ("Components", sigmapartial),
            "Interfacial_Energy": sigmaavg,
        }
    )

    return res


def SigmaCoherent(
    T, x0, db, comps, phasenames, purevms, intervms=[], limit=[0, 1.0], dx=0.01
):
    """
    Calculate the coherent interfacial energy in alloys.

    Parameters
    -----------
    T: float
        Given temperature.
    x0: list
        Initial alloy composition.
    db : Database
        Database containing the relevant parameters.
    comps : list
        Names of components to consider in the calculation.
    phasenames : list
        Names of phase model to build.    
    limit: list
        The limit of composition for searching interfacial composition in equilibrium.
    purevms: list
        The molar volumes of pure components.
    dx: float
        The step of composition for searching interfacial composition in equilibrium.

    Returns:   
    -----------
    Components：list of str
        Given components.
    Temperature: float
        Given temperature.
    Initial_Alloy_Composition: list
        Given initial alloy composition.
    Interfacial_Composition: list
        Interfacial composition of the grid minimization.
    Partial_Interfacial_Energies: list
        Partial interfacial energies of components.
    Interfacial_Energy: float    
        Requested interfacial energies.

    Return type: xarray Dataset
    """
    phasevm = [MolarVolume(db, phasenames[i], comps, purevms[i])
               for i in range(2)]
    _vmis = InterficialMolarVolume(*phasevm)

    """decorate the _vmis to release the constains on temperature"""
    vmis = [each.decfunc() for each in [wraptem(T, f) for f in _vmis]]

    model = CoherentGibbsEnergy(T, db, comps, phasenames)

    """Chemical potentials in two-phase equilibrium"""
    mueq = model.chemicalpotential(x0)

    """Chemical potentials in two bulk phases"""
    model_phase = [
        CoherentGibbsEnergy(T, db, comps, phasenames[i]) for i in range(len(phasenames))
    ]
    alphafuncs, betafuncs = [each.chemicalpotential for each in model_phase]

    sigma_model = SigmaCoherentInterface(alphafuncs, betafuncs, mueq, vmis)

    components = [each for each in comps if each != "VA"]
    cum = int(len(components) - 1)
    print(
        "\n******************************************************************************\nOpenIEC is looking for interfacial equilibirium coposition.\nFor more information visit https://github.com/openiec/openiec."
    )
    x_s = SearchEquilibrium(sigma_model.objective, [limit] * cum, [dx] * cum)
    x_c = ComputeEquilibrium(sigma_model.objective, x_s["x"])
    print(
        "******************************************************************************\n\n"
    )
    sigma = sigma_model.infenergy(x_c)

    xx0 = [1.0 - sum(list(x0))] + list(x0)
    xx_c = [1.0 - sum(list(x_c))] + list(x_c)
    sigmapartial = list(np.array(sigma).flatten())
    sigmaavg = np.average([each for each in sigma])

    res = Dataset(
        {
            "Components": components,
            "Temperature": T,
            "Initial_Alloy_Composition": ("Components", xx0),
            "Interfacial_Composition": ("Components", xx_c),
            "Partial_Interfacial_Energy": ("Components", sigmapartial),
            "Interfacial_Energy": sigmaavg,
        }
    )

    return res
