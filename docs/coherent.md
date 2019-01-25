## Calculating the Coherent Interfacial Energy using OpenIEC

### Prerequisites

- TDB file
- Desired Phases and Components
- Desired Composition (at.) and Temperature (K)

### `SigmaCoherent`
OpenIEC provides the `SigmaCoherent` for the calculation of the coherent interfacial energy in alloys. Parameters and return values are listed as following:

```python
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
```