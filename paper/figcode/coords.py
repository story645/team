#https://stackoverflow.com/questions/39408794/python-3d-pyramid
#https://stackoverflow.com/questions/36675885/rounding-the-edges-of-a-cylinder-in-matplotlib-poly3d
import numpy as np
#x, y, z
verts = [[-1, -1, -1], 
         [1, -1,  -1], 
         [1, 1,  -1 ], 
         [-1, 1, -1],
         [-1, -1, 1], 
         [1, -1, 1 ],
         [1, 1, 1], 
         [-1, 1, 1]]
V = np.array(verts)

nx = 1000
r = .5
bz = 1
tz = 2

t = np.linspace(0, 2*np.pi, nx)
CT = np.vstack((r*np.cos(t), r*np.sin(t), np.ones(nx)*tz)).T

sides = {'TOP': [V[5], V[6], V[7], V[8]], 
         'F1': [V[1], V[2], V[6], V[5]], 
         'F2': [V[2], V[3], V[7], V[6]],
         'F3': [V[3], V[4], V[8], V[7]], 
         'F4': [V[4], V[1], V[5], V[8]], 
         'B1':[V[1], V[0], V[2]],
         'B2':[V[2], V[0], V[3]],
         'B3':[V[3], V[0], V[4]], 
         'B4':[V[4], V[0], V[1]], 
         'CT': CT, 
        }

nphi, nz = 70, 2
r = 0.5  # radius of cylinder
phi = np.linspace(0, 360, nphi) / 180.0 * np.pi
z = np.linspace(1, 2, nz)

PHI, Z = np.meshgrid(phi, z)
CP = r * np.cos(PHI)
SP = r * np.sin(PHI)
XYZ = np.dstack([CP, SP, Z])
verts = np.stack(
    [XYZ[:-1, :-1], XYZ[:-1, 1:], XYZ[1:, 1:], XYZ[1:, :-1]], axis=-2).reshape(-1, 4, 3)

faces = list(sides.values( )) + verts.tolist()

#http://colorpeek.com/#f7e654,82c969,50a387,40718b,414583,43206a
colors = {'TOP':'#F7E654',
         'F1':  '#82C969',
         'F2': '#50A387',
         'F3': '#40718B',
         'F4':'#414583',
         'B1': '#40718B',
         'B2': '#414583',
         'B3': '#82C969',
         'B4': '#50A387',
         'CT': '#F7E654'}

facecolors = list(colors.values()) + ['#43206A'] * len(verts)