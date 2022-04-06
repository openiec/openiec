from openiec.calculate.calcsigma import SigmaPure, SigmaSolLiq
from openiec.property.molarvolume import MolarVolume
from pycalphad import Database


def test():
    """
    Calculate solid/liquid interfacial energies of the Ni-Al system.
    """
    # Given temperature.
    T = 916
    # Given initial alloy composition. x0 is the mole fraction of Ni.
    x0 = [0.01] 
    # Render thermodynamic database.
    db = Database("AlNiAnsara1997.TDB")
    # Define components in the interface.
    comps = ["AL", "NI"]
    # Two phases separated by the interface.
    phasenames = ["FCC_A1", "LIQUID"]

    # Molar volumes of pure components to construct corresponding molar volume database.
    # Molar volume of Al.
    val = "10.269*10.0**(-6.0) + (3.860*10.0**(-5)*10.0**(-6.0))*T**1.491"
    # Molar volume of Ni.
    vni = "6.718*10.0**(-6.0) + (2.936*10.0**(-5)*10.0**(-6.0))*T**1.355"
    purevms = [[val, vni], [val, vni]]

    # A composition range for searching initial interfacial equilirium composition.
    limit = [10 ** (-20), 0.2]
    # The composition step for searching initial interfacial equilirium composition.
    dx = 0.01

    # Call the module for calculating solid/liquid interfacial energies.
    sigma = SigmaSolLiq(
        T=T,
        x0=x0,
        db=db,
        comps=comps,
        phasenames=phasenames,
        purevms=purevms,
        limit=limit,
        dx=dx,
    )
    
    # Print the calculated interfacial energy with xarray.Dataset type.
    print(sigma, "\n")
    # Print the calculated interfacial energy with xarray.DataArray type.
    print(sigma.Interfacial_Energy, "\n")
    # Print the calculated interfacial energy value.
    print(sigma.Interfacial_Energy.values)

    # Output
    """
    <xarray.Dataset>
    Dimensions:                     (Components: 2)
    Coordinates:
    * Components                  (Components) <U2 'AL' 'NI'
    Data variables:
        Temperature                 int32 916
        Initial_Alloy_Composition   (Components) float64 0.99 0.01
        Interfacial_Composition     (Components) float64 0.996 0.003965
        Partial_Interfacial_Energy  (Components) float64 0.1592 0.1592
        Interfacial_Energy          float64 0.1592

    <xarray.DataArray 'Interfacial_Energy' ()>
    array(0.15920587)

    0.15920587414023074
    """


if __name__ == "__main__":
    test()
