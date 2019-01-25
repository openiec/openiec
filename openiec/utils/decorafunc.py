"""
Decorate the f to release the constains on temperature.
"""


def wraptem(T, f):
    def g(x):
        v = f(x, T)
        return v

    return g
