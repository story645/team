import functools

import numpy as np 
#taus

#TODO: write atleast_1d wrapper
class Identity:
    @staticmethod
    def __call__(value):
        return np.array(value)

    @staticmethod
    def validate(mtype):
        return mtype in ['nominal', 'ordinal', 'interval', 'ratio']

class Log:
    def __init__(self, base=10):
        self.base = base

    def __call__(self, value):
        return np.log(value)/np.log(self.base)

    def validate(self, mtype):
        return True
    
class Nominal:
    def __init__(self, mapping):
        self._mapping = mapping
        self._inverse = {v:k for k, v in mapping.items()}
        
    def __call__(self, value):
        values = np.atleast_1d(np.array(value, dtype=object))
        return np.array([self._mapping[v] for v in values])

    def inverse(self, value):
        return self._inverse[value]

    def validate(self, mtype):
        return True

    