## Calculating the Solid/Liquid Interfacial Energy using OpenIEC

### Prerequisites

- TDB file
- Desired Phases and Components
- Desired Composition (at.) and Temperature (K)

### `SigmaSolLiq`
OpenIEC provides the `SigmaSolLiq` for the calculation of the solid/liquid interfacial energy in alloys. Parameters and return values are listed as following:

```python
def SigmaSolLiq( 
    T, x0, db, comps, phasenames, purevms, intervms=[], omega=[], meltingenthalpy=[], sigma0=[], 
    xeq=[], limit=[0, 1.0], dx=0.01,
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
            where "1.0*T" and "2.0*T" are molar volumes of components Ni and Al in FCC_A1 
            phase, while "3.0*T" and "4.0*T" are molar volumes of components Ni and Al in LIQUID phase.
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
```
### `SigmaPure`
OpenIEC provides the `SigmaPure` for the calculation of the solid/liquid interfacial energy in pure metals. Parameters and return values are listed as following:

```python
def SigmaPure(
    T, purevm, db=None, comp=None, phasenames=[], meltingenthalpy=None
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
```