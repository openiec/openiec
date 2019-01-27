## Molar Volume
The molar volumes of different phases are also described as composition- and temperature- dependent properties following the CALPHAD formalism in OpenIEC.

### Prerequisites

- TDB file
- Desired Phases and Components
- Molar volumes of the components

### `MolarVolume`
OpenIEC provides the `MolarVolume` to construct molar volumes of bulk phases. Currently, only contribution of the molar volume of the pure component is considered in OpenIEC. Users can customize the desired molar volume of the bulk phase if the excess molar volume is considerd. Parameters and return values are listed as following:

```python
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
```