import numpy as np

import matplotlib.colors as mcolors

from matplottoy.encoders import mtypes

class Identity:
    @staticmethod
    def validate(mtype):
        return mtype in ['nominal']
        
    @staticmethod
    def __call__(value):
        values = np.atleast_1d(np.array(value, dtype=object))
        return [mtypes.RGBA(*mcolors.to_rgba(v)) for v in values]

class Nominal:
    def __init__(self, mapping):
        """goal of init is to store parameters that would otherwise be
        curried higher level function"""
        assert(mcolors.is_color_like(color) for color in mapping.values())
        self._mapping = mapping
        self._inverse = {v:k for k, v in mapping.items()}

    def __call__(self, value):
        values = np.atleast_1d(value)
        return [mtypes.RGBA(*mcolors.to_rgba(self._mapping[v])) for v in values]

    def inverse(self, value):
        return self._inverse[value]

