from dataclasses import dataclass
from typing import Tuple, Optional, List

import numpy as np
import pandas as pd

# index is like the sheaf, stalk is either the fiber or the values? 
# check the applied category theory book 
# index is subset on K
# technically this can be wrapped even more
# 
# maybe make a Record type Record = {Fiber_Name: values} 
class FruitFrameWrapper:
    F = {'fruit': 'nominal',
         'calories': 'ratio', 
         'juice': 'nominal'}

    def __init__(self, section: pd.DataFrame):
        self.global_section = section

    def query(self, data_bounds:Optional[dict] = None, sampling_rate:int=None)->List[dict]:
        data_bounds = {} if data_bounds is None else data_bounds
        local = self.global_section
        #iter tools chain from iterables probably
        for fibers, bounds in data_bounds.items():
            for Fi, bound in zip(fibers, bounds):
                if bound is None:
                    continue # no selection needed
                if self.F[Fi] == 'nominal':
                    local = local[local[Fi].isin(bound)]
                elif self.F[Fi] == 'ratio':
                    local = local[(min(bound)<=local[Fi]) & (local[Fi]<=max(bound))]
        
        records = {Fi:local[Fi].values.squeeze() for Fi in local.columns}
        return [records]