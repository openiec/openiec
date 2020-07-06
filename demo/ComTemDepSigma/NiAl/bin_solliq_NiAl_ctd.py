from openiec.calculate.calcsigma import SigmaPure, SigmaSolLiq
from openiec.property.molarvolume import MolarVolume
from pycalphad import Database
import numpy as np


def test():
    """
    Calculate solid/liquid interfacial energies of the Ni-Al system.
    """
    # Read the data of compisitons and ttemperatures from a .txt file.
    data = np.genfromtxt("NiAl-xal-tem.txt")
    m, n = data.shape

    # Create a .txt file to store the calculated result.
    output = open("./sigma-NiAl.txt", "w")
    for i in range(m):
        # Given temperature.
        T = data[i][1]
        # Given initial alloy composition. x0 is the mole fraction of Al.
        x0 = [data[i][0]]
        # Render thermodynamic database.
        db = Database("NiAlCrHuang1999.tdb")
        # Define components in the interface.
        comps = ["NI", "AL", "VA"]
        # Two phases separated by the interface.
        phasenames = ["FCC_A1", "LIQUID"]

        # Molar volumes of pure components to construct corresponding molar volume database.
        # Molar volume of Ni.
        vni = "6.718*10.0**(-6.0) + (2.936*10.0**(-5)*10.0**(-6.0))*T**1.355"
        # Molar volume of Al.
        val = "10.269*10.0**(-6.0) + (3.860*10.0**(-5)*10.0**(-6.0))*T**1.491"
        purevms = [[vni, val], [vni, val]]

        # A composition range for searching initial interfacial equilirium composition.
        limit = [10 ** (-20), 0.3]
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
        
        # The given initial alloy composition
        InitialAlloyCompositionValue = sigma.Initial_Alloy_Composition.values
        # The calculated interfacial composition.
        InterfacialCompositionValue = sigma.Interfacial_Composition.values
        # The calculated partial interfacial energy values.
        PartialSigmaValue = sigma.Partial_Interfacial_Energy.values
        # The calculated interfacial energy value.
        SigmaValue = sigma.Interfacial_Energy.values

        # Write the calculated result into the created file.
        output.write("%s%s" % ("%.12e\t"*8, "\n") % (
            T, 
            InitialAlloyCompositionValue[0], InitialAlloyCompositionValue[1], 
            InterfacialCompositionValue[0], InterfacialCompositionValue[1],
            PartialSigmaValue[0], PartialSigmaValue[1],
            SigmaValue
        ))
    output.close()

if __name__ == "__main__":
    test()
