"""
Decorate the f to release the constains on temperature.
"""


class wraptem(object):
    def __init__(self, T, func):
        self.T = T
        self.func = func

    def decfunc(self):
        def g(x):
            return self.func(x, self.T)
        return g
