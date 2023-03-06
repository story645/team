# https://github.com/matplotlib/matplotlib/issues/21688#issuecomment-974912574
import numpy as np

import matplotlib.pyplot as plt

import matplotlib.tri as mtri
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from mpl_toolkits.mplot3d import proj3d

import papercolors as pc
from papercolors import colordict as pcd

config = dict(R = .6, N = 100, 
              xo = 0, yo=0,  zb = -.3, #cyl/mob K center
              zm_off = .875, zc_off =.425, # mob & cyl E y offset
              epsilon = np.finfo(float).eps,
              boundary = 2*np.pi/5, #borderfpr trivilizations
              boundary_pad = np.pi/5
             )
config.update(t = np.linspace(0, 2*np.pi, config['N']))

config.update(r1 = np.array([config['t'][0], config['boundary']])-config['boundary_pad']/2, 
              r2 = np.array([config['boundary'], config['t'][-1]])+config['boundary_pad']/2, #trivialization E x
              ry = .35, rh =.5 , #trivilization E y
              lw = 2, ly = .1 #trivialization K lw and y
             )


config.update(zm = np.linspace(-.75, .75, config['N']//5), #mob E z
              zc = np.linspace(config['ry'], config['ry']+config['rh'], config['N']//5), #cyl E
             )
config.update(xB = config['xo'] + config['R']*np.cos(config['t']), # mob/cyl K x 
              yB = config['yo'] + config['R']*np.sin(config['t']), # mob/cyl K y
              tcg = np.meshgrid(config['t'], config['zc'])[0], # cyl E z
              zcg = np.meshgrid(config['t'], config['zc'])[-1],
             )

config.update(mask1 = (config['t']>=config['boundary']-config['epsilon']-.1), #trivialization 2
              mask2 = (config['t']<=config['boundary']+config['epsilon']+.1) #trivialization 1)
             )
config.update(light_base = pc.lighten(pcd['base'], .4),
              light_total = pc.lighten(pcd['total'], .4),
              light_fiber = pc.lighten(pcd['fiber'], .4))

config.update(dark_colors = (pcd['total'], pcd['fiber'], pcd['base']),
              light_colors = (config['light_total'], config['light_fiber'], config['light_base']),
              bundle_color='dimgray')    

config.update(fs=8, tfs=10, ms=15, aws='->') #other plotting configs


class FancyArrowPatch3D(mpatches.FancyArrowPatch):
    def __init__(self, posA, posB, *args, **kwargs):
        mpatches.FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = list(zip(posA, posB))
        
    def do_3d_projection(self, renderer=None):
        xs3d,  ys3d , zs3d, = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return np.min(zs)
        

def setup_bundle_axes(ax, axis='off'):

    ss = ax.get_subplotspec()
    fig = ax.figure
    ax.remove()
    ax = fig.add_subplot(ss, projection='3d')
    ax.set(xlim=(-.55,.55), ylim=(-.55,.55), zlim=(0,1), aspect='equalxy')
    ax.axis(axis)
    ax.view_init(15, 30)
    return ax
    
    
def plot_cylinder(ax, mask, mask_color):
    x = config['xB'][mask]
    y = config['yB'][mask]
    z = np.meshgrid(config['t'][mask], config['zc'])[-1] + config['zc_off']
    ax.plot_surface(x, y, z, color=pc.lighten(mask_color, .25), shade=False)
    return {i:{'x': x, 'y':y, 'z': np.repeat(config['zc'][i], mask.sum())
                                   + config['zc_off']} 
            for i in [0,-1]}

    
def plot_mobius_band(ax, mask, mask_color):
    
    def mobius_xyz(u, v):
        xvals = config['R']*(1 + .5* v * np.cos(u / 2.0)) * np.cos(u) + config['xo']
        yvals = config['R']*(1 + .5* v * np.cos(u / 2.0)) * np.sin(u) + config['yo']
        zvals = 0.5 * v * np.sin(u / 2.0) + config['zm_off']
        return xvals, yvals, zvals
    
    us, vs = np.meshgrid(config['t'][mask], config['zm'])
    us, vs = us.flatten(), vs.flatten()
    tri = mtri.Triangulation(us, vs)

    ax.plot_trisurf(*mobius_xyz(us, vs),
                    triangles = tri.triangles, edgecolor=None, 
                    color=pc.lighten(mask_color, .25), shade=False)
    
    return {i:dict(zip(['x','y','z'], 
                       mobius_xyz(config['t'][mask], config['zm'][i]))) 
            for i in [0, -1]}


def draw_segmented_bundle(ax, plot_total_space, labels):

    bundle_label = [(r"$(\;$", None ), (f"$E_{labels[1]},$", 'total'),
                    (f"$K_{labels[1]},$",'base'), 
                    ("$\pi$,",None), (f"$F_{labels[1]}$", 'fiber'), (")", None)] 
    
    
    fig = ax.figure
    trans = ax.transAxes
    for s, c in bundle_label:
        pad= " " if s.find("(")>-1 else " "
        fs = config['tfs']+2 if ((s.find(")") >-1 or  s.find("(") >-1)) else config['tfs']
        text = ax.text2D(0.25, 1., s+pad, transform = trans, 
                         color=pcd.get(c, config['bundle_color']),
                         ha='center', va='center', fontsize=fs, family='monospace')
        text.draw(fig.canvas.get_renderer())
        ex = text.get_window_extent()
        ex = fig.dpi_scale_trans.inverted().transform_bbox(ex)
        trans = text.get_transform() + \
                mtransforms.offset_copy(mtransforms.Affine2D(), fig=fig, x=ex.width, y=0)
      
     
        


    for (mask, (tc, fc, bc)) in [(config['mask1'], config['light_colors']), 
                             (config['mask2'], config['dark_colors'])]:


        bounds = plot_total_space(ax, mask, tc)
        
        if mask.sum()>79:
            pii =45
            fp = FancyArrowPatch3D(
                (bounds[0]['x'][pii], bounds[0]['y'][pii], bounds[0]['z'][pii]),
                (config['xB'][mask][pii], config['yB'][mask][pii], config['zb']),
                
                                   arrowstyle=config['aws'], mutation_scale=config['ms'], 
                                   color=config['bundle_color'])
            ax.add_artist(fp)
            ax.text3D(config['xB'][mask][pii], config['yB'][mask][pii], 
                      config['zb']+(bounds[0]['z'][pii] - config['zb'])/2, 
                      "$\pi$", fontsize=config['fs'],
                       color=config['bundle_color'], ha='left', va='center')


        for i in [0,-1]:
            ax.plot(bounds[i]['x'], bounds[i]['y'], bounds[i]['z'], 
                          color=tc, zorder=3)
    
        idx = np.round(np.linspace(0, mask.sum()-1, mask.sum()//4)).astype(int)

        for j, t0 in zip(idx, config['t'][mask][idx]):

            color = 'none' if 0.6*np.pi<t0<1.6*np.pi else fc

            ft = FancyArrowPatch3D((bounds[0]['x'][j], bounds[0]['y'][j], bounds[0]['z'][j]), 
                                      (bounds[-1]['x'][j], bounds[-1]['y'][j], bounds[-1]['z'][j]),
                                       arrowstyle=config['aws'], color=color, mutation_scale=10)
            ax.add_patch(ft)

            ax.plot(config['xB'][mask], config['yB'][mask],  config['zb'], 
                          color=bc, mfc='none', lw=2, markevery=[0, -1], 
                          marker='o', markersize=5)
        


   
    axins = ax.inset_axes([0,-.25, 1, .25])
    axins.axis('off')
    axins.set(xlim=(0,1), ylim=(0,1))
    
    bottom = .4
    top = 1
    
    flip= not np.all(bounds[-1]['z']>bounds[0]['z'])
    t1 = (.15, .33, .77, .9)
    t2 = (t1[1], .5, .6, t1[2]) #inner trivialization
    
    for xm in [t1[1], t1[2]]:
        axins.axvline(xm, bottom, top, linestyle=':', color=pcd['total'], 
                                                gapcolor=config['light_total'])
            
    for (x0, x1, x2, x3), (tc, fc, bc) in [(t1, config['light_colors']), (t2, config['dark_colors'])]:

        for (xl, xr) in [(x0,x1),(x2, x3)]:
            
            rec = mpatches.Rectangle((xl,bottom), width=(xr-xl), height= top-bottom, 
                                 edgecolor=tc, facecolor=pc.lighten(tc, .25))
            axins.add_patch(rec)

            nf = 4 if (xl, xr) == t1[:2] else 3 
            for xa in np.linspace(xl, xr, nf):
                ys, yt = (top, bottom) if flip and xr==t2[1] else (bottom, top) 
                at = mpatches.FancyArrowPatch(posA=(xa, ys), posB=(xa, yt),
                                              arrowstyle='->,head_width=.15', mutation_scale=10, 
                                              edgecolor=fc, zorder=3)
                axins.add_patch(at)
       

            ys, yt = (top, bottom) if flip and xr==t2[1] else (bottom, top) 
            at = mpatches.FancyArrowPatch(posA=(xa, ys), posB=(xa, yt),
                                          arrowstyle='->,head_width=.15', 
                                          edgecolor=fc, zorder=3)
            axins.add_patch(at)

        title = axins.text(.5, 0.075, f"{labels[0]} Bundle", color='k', 
                 fontsize=config['fs'], ha='center', va='bottom')
        
def plot_local_trivialization(ax):
 
    ax.set( ylim=(0, 1), xlim=(config['t'][0]-config['boundary_pad']*2,
                                     config['t'][-1]+config['boundary_pad']*2))
    
    ax.set_title("Local Trivializations of " +r"$(E,K,\pi,F)$", 
                 fontsize=config['tfs'], color='k', y=.9)

    for i, ((x0, x1), (tc, fc, bc)) in enumerate([(config['r1'], config['dark_colors']), 
                                   (config['r2'], config['light_colors'])]):
        rect = mpatches.Rectangle((x0, config['ry']), height = config['rh'], 
                                  width=(x1-x0), 
                                  edgecolor=tc, facecolor=pc.lighten(tc,.25), 
                                  lw=config['lw'])
        ax.add_patch(rect)
        ax.plot([x0, x1], [config['ly'], config['ly']], lw=config['lw'], 
                          color=bc, marker='o', mfc='white',  markersize=4)

        for x in np.linspace(x0, x1, int(np.round(x1-x0,1)*5) +1):
            at = mpatches.FancyArrowPatch(posA=(x, config['ry']), 
                                          posB=(x, config['ry']+ config['rh']),
                                            arrowstyle='->,head_width=0.15', 
                                          mutation_scale=10, edgecolor=fc)
            ax.add_patch(at)
            
        xarr = x0+(x1-x0)*.3
        fp = mpatches.FancyArrowPatch(posA=(xarr, config['ry']), 
                             posB=(xarr, 0.1), 
                               arrowstyle=config['aws'], mutation_scale=config['ms']-5, 
                               color=config['bundle_color'])
        ax.add_artist(fp)
        ax.annotate(text="$\pi$", xy=(0,.5), xycoods=fp,  fontsize=config['fs'],
                   color=config['bundle_color'], ha='left', va='center')
        
        #ax.text(xarr+.1, config['ry']*.75, "$\pi$", fontsize=config['fs'],
        #           color=config['bundle_color'], ha='left', va='center')
        
        xoff=.2*np.math.pow(-1, i+1)
    
       
        ha = ['left', 'right']
        trans = mtransforms.blended_transform_factory(ax.figure.transFigure, ax.transData)
        xp = config['xp'][i]
        ax.text(xp, config['ry']+config['rh'], f"$E_{i}$", color=tc, 
                fontsize=config['tfs'], ha=ha[i], va='top', transform=trans)
        ax.text(xp, config['ry'], f"$F_{i}$", color=fc, 
                fontsize=config['tfs'], ha=ha[i], va='bottom', transform=trans)
        ax.text(xp, 0.1, f"$U_{i}$", color=bc, 
                fontsize=config['tfs'], ha=ha[i], va='center', transform=trans)

       
            
    ax.set(xticks=config['r1'],
                     xticklabels=[r"$\epsilon^{-}$", r"${\dfrac{2\pi}{5}}^{+}$"])


    ax.xaxis.set_minor_locator(mticker.FixedLocator(config['r2']))
    ax.xaxis.set_minor_formatter(mticker.FixedFormatter([r"${\dfrac{2\pi}{5}}^{-}$", r"$\epsilon^{+}$"]))

    ax.tick_params('x', which='major', labelcolor=pcd['base'], 
                             length=0, labelsize=config['fs']-2)
    ax.tick_params('x', which='minor', labelcolor=config['light_base'], 
                             length=0, labelsize=config['fs']-2)
    ax.tick_params('y', labelleft=False, left=False)
    ax.spines[:].set_visible(False)

