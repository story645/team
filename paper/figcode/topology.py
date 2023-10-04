import numpy as np

import matplotlib.colors as mcolors

import intro_plots as ip
from papercolors import colordict as pcd

def make_map():
    pass

def make_timeseries(axt, axk, timeseries):
    for station, dft in timeseries.items():
        dft.plot(ax=axt, color=ip.airports[station]['color'], legend=False)
    axt.set_xlabel(None)
    
    axk.hlines(.5, 0, .75, lw=5, color=pcd['base'])
    axk.axis('off')
    axt.spines.right.set_visible(False)
    axt.spines.top.set_visible(False)
    
def make_table(axt, axk, sample):
    x = np.linspace(-0.25, 1.25, 5)
    shuf = [2,0,3,1,4]
    y=np.repeat(.5, 5)
    yjit = y + [-.1, .05, .1, .15, -.02]
    xshuf = x[shuf]
    
    tab = ip.plot_table(axt, sample, ccolors=['k']*3, 
                        edgecolor=pcd['section'])
    #fig.canvas.draw()

    [tab[0,c].get_text().set_color(pcd['fiber']) for c in range(3)]

    for i, (sn, xi, yi) in enumerate(zip(sample['NAME'], x,y)):
        xt, yt = ip.source_cell(tab[i+1,0],'k', xr=(i/10)+.5)
        station = tab[(i+1,0)].get_text().get_text()
        for c in range(3):
            tab[(i+1,c)].set_facecolor(ip.airports[station]['color'])
            tab[(i+1,c)].set_alpha(.25)
            tab[(i+1,c)].get_text().set_color("black")
            tab[(i+1,c)].get_text().set_wrap(True)

    for i, (xj, yj) in enumerate(zip(xshuf, yjit)):
        station = tab[(i+1,0)].get_text().get_text()
        axk.scatter(xj, yj, s=250, color=mcolors.to_rgba(ip.airports[station]['color'], alpha=1), 
                        edgecolor=pcd['base'], lw=2, zorder=10)

    axk.set(xlim=(-0.5, 1.5), ylim=(.25, .75))
    axk.axis('off')
    axt.axis('off')                             
                                              
def make_plot(sout, dims=None, paper=False):
    dims = [] if dims is None else dims
    mosaic = [['function', 'image'], ['1D', '2D'],[ 'table', 'nodes'], ['net', 'net']]
    fig, axd = plt.subplot_mosaic(mosaic, figsize=(8,8), facecolor='white')
       
    for ax in axd.values():
        ax.axis('off')
        ax.set_facecolor('white')

                
    if 'function' in dims:
        axd['function'].text(0.5, 0.5, r'$f(x)=\frac{1}{\sqrt{2\pi}}e^{x^2}$', transform=axd['function'].transAxes, fontsize=30, ha='center', va='center')
        x = np.linspace(-5,5,10000)
        y = lambda x: (1/np.sqrt(2*np.pi))*np.e**(-x**2/2)
        axd['function'].plot(x, y(x), alpha=.5, lw=10, color=pcd['section'])
        axd['function'].set(xlim=(-5,5))
    
    if '1D' in dims:
        axd['1D'].plot([-5,5], [.5, .5], color=pcd['base'], lw=10)
        axd['1D'].set(xlim=(-5, 5), ylim=(.25, .75))


    if 'image' in dims:
        nrows, ncols = np.array(mosaic).shape
        loc = (np.ravel(mosaic)=='image').nonzero()[0][0] + 1
        axd['image'] =  plt.subplot(nrows, ncols, loc, projection=ccrs.Robinson())
        axd['image'].stock_img()
        axd['image'].coastlines()

    if '2D' in dims:
        r = mpatches.Rectangle((.25,.25), .5, .5, color=pcd['base'])
        axd['2D'].add_artist(r)

    fig.savefig(sout, bbox_inches='tight', facecolor='white', edgecolor='black')
    plt.show()
    return axd