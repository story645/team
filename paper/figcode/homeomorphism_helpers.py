import pandas as pd
import geopandas as gpd
import numpy as np

import metpy
from metpy.interpolate import interpolate_to_grid

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.text as mtext
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import proj3d

import cmocean

import intro_plots as ip
import papercolors
from papercolors import colordict as pcd

mpl.rcParams['font.family'] = 'dejavu sans'
mpl.rcParams['figure.dpi'] = 200
fs={'normal': 10, 'small':9, 'footnote':8, 'script':7, 'tiny':5, 'heading':12}

airports = {'map_date': '20220609',
            'map_color': 'sienna',
            't_lon': -73.7992,
            't_lat': 42.7472,
            'time_color': 'deepskyblue',
            'point_date': '20220309',
            'point_color': 'thistle',
            'jfk_lon': -73.7639,
            'jfk_lat': 40.6392,
            'jfk_color': 'steelblue',
            'lga_lon': -73.8803,
            'lga_lat': 40.7794,
            'lga_color': 'lightskyblue'}
airports.update({'time_point_color': mcolors.to_hex(papercolors.lighten(airports['time_color'], 2))})

def get_data(path):
    df = pd.read_parquet(path)
    dates = df['DATE'].sort_values().unique()
    lons = df['LONGITUDE'].sort_values().unique()
    lats = df['LATITUDE'].sort_values().unique()

    df['DATE_DTYPE'] = pd.to_datetime(df['DATE'])
    prp = df[df['NAME'].isin(['LAGUARDIA AP', 'JFK INTL AP', 'ALBANY INTL AP']) 
             & (df['DATE_DTYPE'].dt.month==3)].pivot_table(
                columns="NAME", index='DATE_DTYPE', values= 'PRCP')
    
    pdf = df.pivot(index='DATE_DTYPE', columns = 'NAME', values = 'PRCP')
    return {'dates':dates, 'lons':lons, 'lats':lats, 'df': df}

def get_timeseries(df, t_lat, t_lon):
    ts = df[(df['LATITUDE'] == t_lat) & (df['LONGITUDE'] == t_lon)].sort_values(by='DATE')
    ts['DATE_DTYPE'] = pd.to_datetime(ts['DATE'])
    return ts

def get_mapdata(mapfile, geofile, map_date):
    mdf = pd.read_csv(mapfile)
    gdf = gpd.read_file(geofile)
    nyshp = gdf[gdf['STATE'].str.match('NY')]
    nyg = mdf[(mdf['DATE'].astype(str) == airports['map_date'])]
    nygeo = gpd.GeoDataFrame(nyg, geometry=gpd.points_from_xy(nyg['LONGITUDE'], nyg['LATITUDE']), crs='EPSG:4269')
    return nygeo, nyshp
    
def make_voxels(dates, lons, lats):
    i, j, k =  np.meshgrid(dates, lons, lats)
    vox_shape = (lons.size, dates.size, lats.size)
    filled = np.zeros(vox_shape, dtype='bool') 
    colors = np.empty(vox_shape, dtype= object)
    edgecolors = np.empty(vox_shape, dtype=object)
    
    # plane: fixed time
    mp = (i == airports['map_date'])
    filled[mp] = 1
    colors[mp] = airports['map_color']
    
    
    # timeseries: fixed lat and lon 
    time = (j == airports['t_lon']) & (k == airports['t_lat']) 
    filled[time] = 1
    colors[time] = airports['time_color']
    #edgecolors[lga] = lga_color
    alb = ((i==airports['point_date']) & (j==airports['t_lon']) & (k == airports['t_lat']))
    edgecolors[alb] = airports['time_point_color']
    # points  - compare two stations
    jfk = ((i==airports['point_date']) & (j==airports['jfk_lon']) & (k==airports['jfk_lat']))
    filled[jfk] = 1
    colors[jfk] = airports['jfk_color']
    #edgecolors[jfk] = jfk_color
    lga = ((i==airports['point_date']) & (j ==airports['lga_lon']) & (k == airports['lga_lat']))
    filled[lga]= 1
    colors[lga] = airports['lga_color']
    
    return filled, colors, edgecolors

def make_cube(dates, lons, lats, ax):
    x0, x1 = 0, len(lons)
    y0, y1 = 0, len(dates)
    z0, z1 = 0, len(lats)
    
    #lon, date, fixed z
    xy1 = [(x0, y0, z0), (x0, y1, z0),  (x1, y1, z0), (x1, y0, z0)]
    xy2 = [(x0, y0, z1), (x0, y1, z1),  (x1, y1, z1), (x1, y0, z1),]
    #lat, date, fixed x
    yz1 = [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1),  (x0, y1, z0)]
    yz2 = [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1),  (x1, y1, z0)]
    # lon, lat, fixed y
    xz1 = [(x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0)]
    xz2 = [(x0, y1, z0), (x0, y1, z1),(x1, y1, z1),  (x1, y1, z0)]
    
    z_less = [xy1, xz2, yz1]
    z_more = [xy2, xz1, yz2]
    
    cube_front = Poly3DCollection(z_more, facecolor=('lavender', .5), edgecolor=pcd['base'], ls=':', zorder=20)
    ax.add_collection3d(cube_front)

    filled, colors, edgecolors = make_voxels(dates, lons, lats)
    vox = ax.voxels(filled, facecolors = colors, edgecolors=edgecolors, ls='--', shade=None, alpha=1, zorder=10)
    
    # project the date on the date axes so     
    y_ind = np.where(dates==airports['point_date'])[0]
    p_alpha = .75
    # y is the date, z is latitude +- where, longitude is lost, x is fixed at x0
    for p_lat, p_color in [(airports['jfk_lat'], airports['jfk_color']), 
                           (airports['lga_lat'], airports['lga_color']), 
                           (airports['t_lat'], airports['time_point_color'])]:
        p_ind = np.where(lats == p_lat)[0]
        ax.plot((x0, x0), (y_ind, y_ind), (p_ind, p_ind + 1), color=p_color, alpha=p_alpha)
    span_ind = np.where(lats == airports['t_lat'])[0]

    ax.plot((x0,x0), (y_ind, y_ind), (z0, x1), color=airports['point_color'], alpha=p_alpha, zorder=-1)

    
    N = 10
    t_ind = np.where(dates==airports['map_date'])
    poly_alpha = p_alpha - .25
    ax.fill_between(x0, np.linspace(y0, t_ind, N), span_ind, x0, np.linspace(y0, t_ind, N), span_ind+1, facecolor=airports['time_color'],  alpha=poly_alpha, edgecolor= None, zorder=-30)

    #fake the lines to get the correct zorder
    ax.plot((x0, x0),(y1, y1), (z0, z1), color=cube_front.get_ec(), ls=cube_front.get_ls()[0], zorder=-10, lw=cube_front.get_lw())
    ax.plot((x0, x0),(y0, y1), (z0, z0), color=cube_front.get_ec(), ls=cube_front.get_ls()[0], zorder=-10, lw=cube_front.get_lw())
    ax.plot((x0, x1),(y1, y1), (z0, z0), color=cube_front.get_ec(), ls=cube_front.get_ls()[0], zorder=-10, lw=cube_front.get_lw())
    ax.view_init(15, -50, None)
    ax.axis('off')
            
    
            
    ax.text(x0, y0+y1/2, z1, "date", zdir='y', va='bottom', ha='center', size=fs['normal'])
    ax.text(x1, y1, z0 + z1/2, "latitutude", zdir='z', ha='center', va='top', rotation=90, 
            transform_rotates_text=True, rotation_mode='anchor', size=fs['normal'])
    ax.text(x0+x1/2, y1, z1, "longitude", zdir='x', va='bottom', ha='center', size=fs['normal'] )
    return vox

def make_ts(df, ax):
    ts = get_timeseries(df, airports['t_lat'], airports['t_lon'])
    
    ln,  = ax.plot('DATE_DTYPE', "PRCP", data=ts, color = airports['time_color'])
    ax.axvline(pd.to_datetime(airports['point_date']), color=airports['point_color'], alpha=.75, zorder=-1)
    ax.set_xlim(xmin=ts['DATE_DTYPE'].min(), xmax=ts['DATE_DTYPE'].max())
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.annotate("2002", (1, -0.1), xycoords='axes fraction', 
                fontsize=fs['footnote'], va='top', ha='center')
    return ln 
    
def make_bars(df, ax1):    
    ax1.set_title(pd.to_datetime(airports['point_date']).strftime(format="%b %d"), 
                  color=papercolors.lighten(airports['point_color'], 2), size=fs['small'])
    jfk = df[(df['DATE']==airports['point_date']) & (df['LATITUDE'] == airports['jfk_lat']) & (df['LONGITUDE'] == airports['jfk_lon'])]
    lga = df[(df['DATE']==airports['point_date']) & (df['LATITUDE'] == airports['lga_lat']) & (df['LONGITUDE'] == airports['lga_lon'])]
    ts = get_timeseries(df, airports['t_lat'], airports['t_lon'])
    vals = [jfk['PRCP'].values[0], lga['PRCP'].values[0], ts[ts['DATE']==airports['point_date']]['PRCP'].values[0]]
    bars = ax1.bar(["JFK", "LGA", "ALB"], vals, color=[airports['jfk_color'], airports['lga_color'], airports['time_color']])
    print(vals)
    return bars

def make_map(nygeo, nyshp, ax, colorbar=True, square=True, label=True):
    px, py, prcp = interpolate_to_grid(nygeo['LONGITUDE'].values, nygeo['LATITUDE'].values, nygeo['PRCPI'].values, 
                                       interp_type='barnes', minimum_neighbors=3, 
                                             search_radius=.25, hres=.025, gamma=1)
    cmap = cmocean.cm.rain
    norm = mcolors.Normalize(vmin=0, vmax=1)
    nyshp.plot(ax=ax,  facecolor='#f6f5f7' , edgecolor='none')
    im = ax.pcolormesh(px, py, prcp, cmap=cmap, norm=norm, alpha=.8)
    mp = nyshp.plot(ax=ax,  facecolor='none', edgecolor=airports['map_color'])
    if square:
        for p_id, p_color in [('JFK INTL AP', airports['jfk_color']), ('LAGUARDIA AP', airports['lga_color']), ('ALBANY INTL AP', airports['time_color'])]:
            nygeo[nygeo['NAME']==p_id].plot(marker ='s',edgecolor=p_color, facecolor='none', ax=ax, markersize=60, lw=2)

    if colorbar:
        cb = ax.get_figure().colorbar(im, ax=ax, fraction=.1, aspect=15, 
                          location='left', extend='max', pad=.001)
        cb.ax.tick_params(labelsize=fs['script'], length=0, pad=2)
        cb.ax.xaxis.set_major_formatter("{:0.2f} in.".format)
    
    ax.axis('off')

    if label:
        ax.annotate(pd.to_datetime(airports['map_date']).strftime("%b %d"), (0.05,1), xycoords= mp, 
                    color=airports['map_color'], fontsize=fs['small'], ha='left', va='top')
    
    return mp, im