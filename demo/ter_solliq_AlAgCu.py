from openiec.calculate.calcsigma import SigmaPure, SigmaSolLiq
from pycalphad import Database


def test():
    """
    Calculate solid/liquid interfacial energies of the Al-Ag-Cu system.
    """
    # Given temperature.
    T = 775.09
    # Given initial alloy composition. x0 is the mole fraction of Al. x0 corresponds to the mole fractions of Ag and Cu.
    x0 = [0.1648, 0.08]
    # Render thermodynamic database.
    db = Database("AlAgCu.TDB")
    # Define components in the interface.
    comps = ["AL", "AG", "CU", "VA"]
    # Two phases separated by the interface.
    phasenames = ["FCC_A1", "LIQUID"]

    # Molar volumes of pure components to construct corresponding molar volume database.
    # Molar volume of Al.
    val = "10.269*10.0**(-6.0) + (3.860*10.0**(-5)*10.0 ** (-6.0))*T**(1.491*10.0**(-6.0))"
    # Molar volume of Ag.
    vag = "10.49*10.0**(-6.0) + (9.646*10.0**(-5)*10.0**(-6.0))*T**(1.314*10.0**(-6.0))"
    # Molar volume of Cu.
    vcu = "7.226*10.0**(-6.0) + (4.06*10.0**(-5)*10.0**(-6.0))*T**(1.355*10.0**(-6.0))"
    purevms = [[val, vag, vcu]] * 2

    # A composition range for searching initial interfacial equilirium composition.
    limit = [10 ** (-20), 0.8]
    # The composition step for searching initial interfacial equilirium composition.
    dx = 0.1

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
    print(sigma.Interfacial_Energy.values, "\n")

    # Output
    """
    <xarray.Dataset>
    Dimensions:                     (Components: 3)
    Coordinates:
    * Components                  (Components) <U2 'AL' 'AG' 'CU'
    Data variables:
        Temperature                 float64 775.1
        Initial_Alloy_Composition   (Components) float64 0.7552 0.1648 0.08
        Interfacial_Composition     (Components) float64 0.7834 0.1676 0.04898
        Partial_Interfacial_Energy  (Components) float64 0.1695 0.1695 0.1695
        Interfacial_Energy          float64 0.1695 

    <xarray.DataArray 'Interfacial_Energy' ()>
    array(0.16953083925496695) 

    0.16953083925496695 
    """


if __name__ == "__main__":
    test()
