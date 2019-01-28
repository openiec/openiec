## Calculating the Coherent Interfacial Energy using OpenIEC

### Prerequisites

- TDB file
- Desired Phases and Components
- Desired Composition (at.) and Temperature (K)

**Calculation of the coherent interfacial energy**

- Ni-Al system
- Coherent interfacial energy between FCC_A1 and GAMMA_PRIME
- Temperature: 800 K
- Composition: Ni-20at.%Al
- TDB file: [NiAlHuang1999.tdb](./demo/NiAlHuang1999.tdb)

Import necessary modules from the `pycalphad` and `openiec`. `Database` is a class in `pycalphad` designed to input/output information from `TDB` file. `SigmaCoherent` is a function in `openiec` to construct symbolic expression of interfacial energy for coherent phase. 

```python
from pycalphad import Database
from openiec.calculate.calcsigma import SigmaCoherent
```

Read in the `TDB` file using the utility from `pycalphad`
```python
# Render thermodynamic database.
db = Database("NiAlHuang1999.tdb")
```

Molar volume is one of the prerequisite for computing the interfacial energy, as interfacial area depends its its molar volume when the volume is fixed. One specify the molar volume for all the components for the two phases forming an interface. In the `Ni-Al` system, the molar volume for pure `Ni` is `6.718*10.0**(-6.0) + (2.936*10.0**(-5)*10.0**(-6.0))*T**(1.355*10.0**(-6.0))`, while the molar volume for pure `Al` is `10.269*10.0**(-6.0) + (3.860*10.0**(-5)*10.0**(-6.0))*T**(1.491*10.0**(-6.0))`. It is also assume that the molar volumes for both FCC_A1 and GAMMA_PRIME are the same. Thus, the molar volumes to be input is written as
```python
# Molar volumes of pure components to construct corresponding molar volume database.
purevms = [
    [
        "6.718*10.0**(-6.0) + (2.936*10.0**(-5)*10.0**(-6.0))*T**(1.355*10.0**(-6.0))", 
        "10.269*10.0**(-6.0) + (3.860*10.0**(-5)*10.0**(-6.0))*T**(1.491*10.0**(-6.0))"
    ],
    [
        "6.718*10.0**(-6.0) + (2.936*10.0**(-5)*10.0**(-6.0))*T**(1.355*10.0**(-6.0))", 
        "10.269*10.0**(-6.0) + (3.860*10.0**(-5)*10.0**(-6.0))*T**(1.491*10.0**(-6.0))"
    ],
]
```
`purevms` is a two-dimension array, and each nested array in `purevms` stores the molar volume of the components, in the order of the components being specified in `SigmaCoherent`. The molar volume for `VA` can be omitted.

The next step is create an object of `SigmaCoherent`, where `comps` and `phasenames` has to be specified in order. (**Note** the molar volume mentioned previously should always follow these orders.) The temperature has been set as `800.0` Kelvin. `x0` stands initial alloy composition. As we are dealing with binary system, only the composition for `Al` is in need, while the composition for `Ni` is calculated by `1 - x(Al)`， internally in `openiec`.


```python
# Call the module for calculating coherent interfacial energies.
sigma = SigmaCoherent(
    comps = ["NI", "AL", "VA"], 
    phasenames = ["FCC_A1", "GAMMA_PRIME"], 
    db = db, 
    T = 800.0, 
    x0 = [0.2,], 
    purevms = purevms
)
```

Once everything is ready, the interfacial energy can be calculated conveniently.

```python
# Print the calculated interfacial energy.
print(sigma.Interfacial_Energy.values)

# Result is printed as following
'''
Output: 0.027399568639258774
'''
```

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