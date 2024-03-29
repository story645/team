import numpy as np

import matplotlib as mpl

import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.table as mtable
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

#scatter position: 

airports = {'ALBANY INTL AP': {'code': 'ALB', 'color': '#469990'},
            'BINGHAMTON': {'code': 'BGM', 'color': '#9A6324'},
            'BUFFALO': {'code': 'BUF', 'color': '#f032e6'},
            'GLENS FALLS AP': {'code': 'GFL', 'color': '#dcbeff'},
            'ISLIP-LI MACARTHUR AP': {'code': 'ISP', 'color': '#ffe119'},
            'LAGUARDIA AP': {'code': 'LGA', 'color': '#f58231'},
            'ROCHESTER GTR INTL AP': {'code': 'ROC', 'color': '#800000'},
            'SYRACUSE HANCOCK INTL AP': {'code': 'SYR', 'color': '#aaffc3'},
            'JFK INTL AP': {'code': 'JFK', 'color': '#000075'},
            'HILO INTERNATIONAL AIRPORT': {'code': 'ITO', 'color': '#3CB44B'},
            'BARROW AIRPORT': {'code': 'BRW', 'color': '#C0C0C0'},
            'SARANAC LK ADIRONDACK RGNL AP': {'code': 'a', 'color': '#42d4f4'},
            'STONYKILL NEW YORK': {'code': 'b', 'color': '#fabed4'}}
rac = {v['code']: k for k, v in airports.items()}

ssubset = set(airports.keys()) - {'HILO INTERNATIONAL AIRPORT', 'BARROW AIRPORT'}


def plot_table(ax, dfs, ccolors, edgecolor='k', textcolor='k'):
    tab = mtable.table(ax, cellText=dfs.astype('str').values, cellLoc='center',
                   colLabels=dfs.columns, loc='center')
        #bbox=(0, 0, 1, 1))
    tab.auto_set_font_size(False)
    tab.set_fontsize('medium')
    tab.scale(1.25, 1.5)
    tab.auto_set_column_width(np.arange(len(dfs.columns)))
    for i, color in enumerate(ccolors):
        for j in range(len(dfs)+1):
            if textcolor is None:
                tab[j,i].get_text().set_color(color)
            else:
                tab[j,i].get_text().set_color(textcolor)
            tab[j,i].set_edgecolor(edgecolor) 
    
    ax.set(xticks=[], yticks=[], aspect='equal')
    ax.axis('off')
    ax.add_table(tab)
    return tab

def plot_map(ax, gdf, nystate, cmap, norm, fade='k', alpha=.5, station=None):
    for name in airports:
        a = 1 if name == station else alpha
        df = gdf.loc[[name], ['PRCPI','geometry']]
        df.plot(ax=ax, label=name, facecolor=cmap(norm(df['PRCPI'])), 
                edgecolor=mcolors.to_rgba(airports[name]['color'], alpha=a), 
                legend=False, linewidth=2.5, alpha=a, markersize=100)
    
    nystate[nystate['postal'].str.match('NY')].plot(ax=ax,
                            facecolor='white', edgecolor=fade, zorder=-1)
    
    ax1_divider = make_axes_locatable(ax)
    cax = ax1_divider.append_axes("right", size="5%", pad="2%")
    cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap,norm=norm, orientation='vertical', drawedges=False, alpha=alpha)
    cb.set_label('total precipitation (in.)', 
                 rotation=270, color=fade, labelpad=12)
    for axes in [ax, cax]:
        axes.tick_params(color=fade, labelcolor=fade)
        axes.spines[:].set_color(fade)
    ax.set_aspect('equal')
    ax.axis('off')
    return 
    
def plot_time(ax, df, fade='k', alpha=.5, station=None):
    for name, gdf in df.groupby(['NAME']):
        a = 1 if name == station else alpha
        zorder = 100 if name == station else -1
        ax.plot('DATES', 'PRCPI', data=gdf, label=name, color=airports[name]['color'], alpha=a, zorder=zorder, lw=2)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
    ax.tick_params(color=fade, labelcolor=fade)
    ax.spines[:].set_color(fade)
    ax.set_ylabel('precipitation (in.)', 
                  rotation=270,  color=fade, labelpad=12)
    ax.yaxis.set_label_position('right')
    ax.tick_params('y', labelright=True, labelleft=False, right=False, left=False)
    return 
    
def source_cell(cell, color='k', xr=.5, yr=.5):
    cell.get_text().set_color(color)
    x = cell.get_x() + cell.get_width()*xr
    y = cell.get_y() + cell.get_height()*yr
    return x, y