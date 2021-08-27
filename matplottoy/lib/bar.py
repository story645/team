from __future__ import annotations
from collections import namedtuple
from collections.abc import Iterable
import copy
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Any, Callable, Union


import numpy as np 

from matplotlib import rcParams


import matplotlib.artist as martist
import matplotlib.cbook as cbook
import matplotlib.path as mpath
import matplotlib.transforms as mtransforms

from matplottoy.artists import utils
from matplottoy.encoders import mtypes

# axes artist, line artist, write a fake xlim/ylim 
# matplotlib can roundtrip V->H, H->V (transforms)

# mu = \nu \circ \tau 
#\tau = data.query().projection()

@dataclass
class FtoV:
    nu: Callable
    f: Union[Tuple[str, ...], None] = None
    nu_inv: Union[Callable, None] = None

Vspec= Dict[str, Tuple[Tuple[str,...], FtoV]]
# Spivak's records = sections evaluated on U \subset K
Records = Dict[str, Union[Iterable, Callable]]

class Rho: 
    # rho: S \rightarrow H
    # rho = \q \circ \xi^*(\mu) =? \qhat \circ \mu (over^k)
    
    def __init__(self, V:Optional[Vspec]=None):
        # F->V maps need to be fixed here, but use fiber name instead of function
        self.V = {} if V is None else V

    def mu(self, tau_restricted: Records):
        pass
    
    @staticmethod
    def qhat():
        pass

class TopologicalArtist: 
# also maybe should be owned by data library? 
#is bad name for this since this is more than just qhat
    def __init__(self, graphic:Rho):
        # is parameterized by the rho
        # only input is \tau (E)
        self.graphic = graphic
        self.data = None

    #section has to be ducktyped w/ a query method
    def compose_with_tau(self, section): #doesn't need to be there
        # do I care about bounds yet? or only at draw time?
        new = copy.copy(self)
        new.data = section
        return new

    def query(self, data_bounds:Optional[dict]=None, sampling_rate:Optional[int]=None)->dict:
        return self.data.query(data_bounds, sampling_rate)
        # section.view, #xi seperates nicely 

def barH(V):
    new_key = {'position': 'x', 'height':'y'}
    return Bar({(new_key[k] if k in new_key else k):v for (k, v) in V.items()})

def barV(V):
    new_key = {'position': 'y', 'height':'x'}
    return BarV({(new_key[k] if k in new_key else k):v for (k, v) in V.items()})

class Bar(Rho): 
    #what are the 
    P_required = {'x', 'y'}
    P_optional = {'floor', 'width', 'facecolor', 'edgecolor', 
                  'linewidth', 'linestyle'}

    # Spivak r: C \rightarrow U_{\sigma}, U_{sigma}=F_{i}=F_{c} 
    def compose_with_nu(self, p:str, f:Tuple[str,...], nu:callable, nu_inv:callable=None)->Bar:
        #trying to sort out how to not lose existing specs
        # also maybe type checking here? (Is this nu valid for this fiber?)
        new = copy.copy(self)
        # user needs to do nu_i = nu_i_j \circ nu_i_k composition
        new.V[p] = FtoV(nu=nu, f=f, nu_inv=nu_inv) 
        return new

    def mu(self, tau_restricted: Records)->Records: #draw
        #required nus, also done first to get length
        mus = {p: self.V[p].nu(*(tau_restricted[c] 
                for c in self.V[p].f)) for p in self.P_required}

        N = len(mus[list(self.P_required)[0]]) # length of mus 

        for p in self.P_optional:
            if self.V[p].f is None:
                # don't like this 'cause this is special casing for None
                # also it's mpl enforcing the structure of default nus
                # down in the artist level
                mus[p] = self.V[p].nu(N)
            else:
                mus[p] = self.V[p].nu(*(tau_restricted[c] 
                                        for c in self.V[p].f))
        return mus

    @staticmethod
    def qhat(x, width, y, floor, facecolor, edgecolor, linewidth, linestyle):
        # are matplotlib 
        def fake_draw(render, transform=mtransforms.IdentityTransform()):
            for (xi, wd, yi, fl, fc, ec, lw, ls) in zip(x, width, y, floor, facecolor, edgecolor, linewidth, linestyle):
                gc = render.new_gc()
                gc.set_foreground((ec.r, ec.g, ec.b, ec.a))
                gc.set_dashes(*ls)
                gc.set_linewidth(lw)
                path = mpath.Path([(xi, fl), (xi, fl + yi), 
                           (xi + wd, fl + yi), 
                           (xi + wd, fl), (xi, fl)], closed=True)
                render.draw_path(gc=gc, path=path, 
                    transform=transform, 
                    rgbFace=(fc.r, fc.g, fc.b, fc.a))
        return fake_draw

class BarH(Bar):
    @staticmethod
    def qhat(x, width, y, floor, facecolor, edgecolor, linewidth, linestyle):
        # horizontal bar, x0 is floor, x1 is height, y is y0, width is y1
        return Bar.qhat(floor, x, width, y, facecolor, edgecolor, linewidth, linestyle)


class GenericArtist(martist.Artist):
    # start w/ working w/ an artist object then stripped down artist
    def __init__(self, artist:TopologicalArtist):
        super().__init__()
        self.artist = artist
        self.artist.V['x'] # update w/ transforms ax.transdata.transform
        self.artist.V['y'] # update transform
  
    # rename, this isn't on screen
    # proxy for half xi, VtoF
    # axes is an artist, data in E is bounds
    # axes has nus for those bounds to screen space
    # get data in axes bounds
    # tau_genericArtist_x \subset tau_Axes_x
    # tau_genericArtist_y \subset tau_Axes_y
    # this assumes shared nu
    # mu_genericArtist_x \subset mu_Axes_x
    # get_xlim()/get_ylim = (mu_x, mu_y)
    # genericArtist_nu_preimage(mu_x, mu_y) => genericArtst_tau
    # AxesArtist_nu_preimage(mu_x, mu_y) => AxesArtist_tau
    # get_xlim(), get_ylim() -> 0,1-AxesNu->[100,400]
    # data = nu([50, 20, 19, 290])-DataNu->[100-400]
    # mu [ 100, 200,  400] <- see on screen which is mu
    # Assume that the artist shares a nu with an underlying axes
        # cheat about doing the filtering on f rather than mu
    # can't cheat
        # invert/clean_preimage: get the mu_Axes, preimage through artist_nu, filter back into data
        # handwave as I know about this, but it's out of scopeish
        # no_invertable: no cheat: k = data.query() \subset preimage , data.query(k)
    # matplotlib does not return tau_Axes
    # matplotlib currently gives approx mu_1_Axes 
    # datetime->datetime

    # data gets selection 
    def get_screen_bounds_to_data_bounds(self, renderer)->(dict, int):
        """proxy for S->F over K"""
        # actual limits...scale...projections...
        # x1, x1
        # this should maybe be owned by the data object 
        # since it's so specific
        # render gives you the dpi
        # width in pixels of the data
        # renderer has wiidth and dpi or ask axes
        # axes in screen coordinates or data coordinates
        # how many pixels to up/down sample
        # don't cache it, use it for up and down  
        # we cheat by being in V since we have \Q^{-1}(renderer) as a transfrom.inverted
        # BoundaryNu([5, 6,7, 8, 9]) -> 1 -
        # xlim = 1   
        # nu_preimage(1) = [5,6,7,8,9]
        # x_data_min = min(5,6,7,8,9)
        xmin = min(nu_inv(self.axes.get_xlim()))
        xmax = max
        #assumes that D->V w/o any transforms
        nu = lambda x: x + 2
        mu = d1+2
        axes.get_xlim()->(x0, x1)->(0, 5)
        E-> [0, 5] or [-2, 3]

        #output has to be in dataspace
        return {'x': self.axes.get_xlim(), 
                'y': self.axes.get_ylim()}, renderer.dpi

    def draw(self, renderer):
        # get bounding ax.get_xlim(), ax.get_ylim()
        # get bounding box from coordinates on screen to data coordinates
        # can compute 
        ### assume we have data bounds

        # converts screen to data, there's nu k \in U yet 
        bounding_box, sampling_rate = self.get_screen_bounds_to_data_bounds(renderer)
        # tau: U\subset K \rightarrow F
        #topArtist.graphic.V.items()[0]
        
        # maybe do loop over taus here (local section of taus)
        for tau_restricted in self.artist.data.query(bounding_box, sampling_rate):
            # you write make_mu & qhat so what gets passed into which
            # \qhat \circ mu 
            mu = self.artist.graphic.mu(tau_restricted)
            rho = self.artist.graphic.qhat(**mu)
            H = rho(renderer)