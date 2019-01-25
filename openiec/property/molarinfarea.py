"""
Calculate molar interfacial areas of components.
"""

import numpy as np


def MolarInterfacialArea(vmi, fb=0.65, fi=0.906):
    """
    Calculate molar interfacial areas of components.

    Reference:
        Kaptay G. Materials Science and Engineering: A, 2008, 495(1-2): 19-26.

    Parameters
    -----------
    fb: float
        The packing ratios of bulk phases.
    fi: float
        The packing ratios of the interface.
    vmi: float
        The characteristic molar volumes of pure components at the interface.
    """
    NAv = 6.02 * 10.0 ** 23
    f = ((3.0 * fb / 4.0) ** (2.0 / 3.0)) * ((np.pi ** (1.0 / 3.0)) / fi)
    omega = f * (vmi ** (2.0 / 3.0)) * (NAv ** (1.0 / 3.0))
    return omega
