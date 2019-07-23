from openiec.calculate.calcsigma import SigmaPure
from pycalphad import Database


def pureAlandNi_solliq():
    """
    Calculate the solid/liquid interfacial energies of pure metals.
    """
    # Given temperature.
    T = 839
    # Render thermodynamic database.
    db = Database("AlNiAnsara1997.TDB")
    # Define elements.
    components = ["AL", "NI"]
    # Two phases separated by the interface.
    phasenames = ["FCC_A1", "LIQUID"]

    # Molar volumes for elements.
    # Molar volume of Al.
    val = 10.269 * 10.0 ** (-6.0) + (3.860 * 10.0 ** (-5) * 10.0 ** (-6.0)) * (
        T ** 1.491
    )
    # Molar volume of Ni.
    vni = 6.718 * 10.0 ** (-6.0) + (2.936 * 10.0 ** (-5) * 10.0 ** (-6.0)) * (
        T ** 1.355
    )
    vm = [val, vni]

    # Call the module for calculating solid/liquid interfacial energies in pure metals.
    sigma = [
        float(
            SigmaPure(
                T, vm[i], db, components[i], phasenames=phasenames
            ).Interfacial_Energy.values
        )
        for i in range(len(components))
    ]

    # Print caluated interfacial energy values.
    print(sigma)

    # Output
    """
    [0.15574946600009512, 0.3223878512351404]
    """


def pureAl_solliq():
    """
    Calculate the solid/liquid interfacial energy of pure Al.
    """
    # Given temperature.
    T = 800
    # Render thermodynamic database.
    db = Database("AlNiAnsara1997.TDB")
    # Define the element.
    comp = "AL"
    # Two phases separated by the interface.
    phasenames = ["FCC_A1", "LIQUID"]

    # Molar volumes for elements.
    # Molar volume of Al.
    val = 10.269 * 10.0 ** (-6.0) + (3.860 * 10.0 ** (-5) * 10.0 ** (-6.0)) * (
        T ** 1.491
    )

    # Call the module for calculating solid/liquid interfacial energies in pure metals.
    sigma = SigmaPure(T, val, db, comp, phasenames)

    # Print the calculated interfacial energy with xarray.Dataset type.
    print(sigma, "\n")
    # Print the calculated interfacial energy with xarray.DataArray type.
    print(sigma.Interfacial_Energy, "\n")
    # Print the calculated interfacial energy value.
    print(sigma.Interfacial_Energy.values)

    # Output
    """
    <xarray.Dataset>
    Dimensions:             ()
    Data variables:
        Component           <U2 'AL'
        Temperature         int64 800
        Melting_Enthalpy    float64 1.071e+04
        Interfacial_Energy  float64 0.155 

    <xarray.DataArray 'Interfacial_Energy' ()>
    array(0.15497715523946845) 

    0.15497715523946845
    """


def pureNi_solliq():
    """
    Calculate the solid/liquid interfacial energy of the pure Ni.
    """
    # Given temperature.
    T = 800
    # Render thermodynamic database.
    db = Database("AlNiAnsara1997.TDB")
    # Define the element.
    comp = "NI"
    # Two phases separated by the interface.
    phasenames = ["FCC_A1", "LIQUID"]

    # Molar volumes for elements.
    # Molar volume of Ni.    
    vni = 6.718 * 10.0 ** (-6.0) + (2.936 * 10.0 ** (-5) * 10.0 ** (-6.0)) * (
        T ** 1.355
    )

    # Call the module for calculating solid/liquid interfacial energies in pure metals.
    sigma = SigmaPure(T, vni, db, comp, phasenames)

    # Print the calculated interfacial energy with xarray.Dataset type.
    print(sigma, "\n")
    # Print the calculated interfacial energy with xarray.DataArray type.
    print(sigma.Interfacial_Energy, "\n")
    # Print the calculated interfacial energy value.
    print(sigma.Interfacial_Energy.values)

    # Output
    """
    <xarray.Dataset>
    Dimensions:             ()
    Data variables:
        Component           <U2 'NI'
        Temperature         int64 800
        Melting_Enthalpy    float64 1.748e+04
        Interfacial_Energy  float64 0.3211 

    <xarray.DataArray 'Interfacial_Energy' ()>
    array(0.321081580921721) 

    0.321081580921721
    """


if __name__ == "__main__":
    pureAlandNi_solliq()
    pureAl_solliq()
    pureNi_solliq()
