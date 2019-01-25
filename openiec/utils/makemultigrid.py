"""
Construct the function of generating grid points for grid minimization.
"""


def makemultigrid(dim, gridnums, tol=1.0e-10):
    """
    Generate grid points for grid minimization. The grid is going to be created in a recursive way.

    Parameters
    ----------
    dim: int
        Dimension of the grid.
    gridnumbers: int-tuple
        The grid numbers of all the coordinates.
    """
    # the initial point
    p = [0.0 for i in range(dim)]
    stor = [p]
    for ni in range(dim):
        tstor = []
        for nj in range(1, gridnums[ni] + 1):
            for each in stor:
                pt = each[:]
                pt[ni] = float(nj) / float(gridnums[ni])
                tstor.append(pt)
        for each in tstor:
            stor.append(each)

    for i in range(len(stor)):
        for j in range(len(stor[i])):
            stor[i][j] = tol + (stor[i][j] - tol) * (1.0 - tol)
    return stor
