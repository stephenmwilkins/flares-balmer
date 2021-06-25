import numpy as np


from astropy.io import ascii

import matplotlib as mpl
import matplotlib.cm as cm
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import flares
import flare.plt as fplt


import flare



cosmo = flare.default_cosmo()

norm = mpl.colors.Normalize(vmin=8.5, vmax=10.5)

fesc = 0.0
log10Z = -3




fig, ax = fplt.simple(size=3.5)

line_styles = ['-','--']

for i, sfh_type in enumerate(['constant', 'instant']):

    ls = line_styles[i]

    for j, log10tau_V in enumerate([-5., -1.0, -0.3, 0.0]):
        c = cm.magma(j/4)
        tau_V = np.round(10**log10tau_V, 1)
        data = ascii.read(f'data/{sfh_type}_fesc{fesc}_log10Z{log10Z}_tauV{tau_V}.dat')
        C = -2.5*np.log10(data['FAKE.FAKE.BBa']/data['FAKE.FAKE.BBb'])
        ax.plot(data['log10_duration'], C, c=c, lw=1, ls=ls, label = fr'$\rm \tau_{{V}}={tau_V}$')


    # add f_esc = 1.0
    data = ascii.read(f'data/{sfh_type}_fesc1.0_log10Z{log10Z}.dat')
    C = -2.5*np.log10(data['FAKE.FAKE.BBa']/data['FAKE.FAKE.BBb'])
    ax.plot(data['log10_duration'], C, c='0.5', lw=1, ls=ls, label = r'$\rm f_{esc}=1$')


# z = 4
# t_uni = np.log10(cosmo.age(z).to('yr').value)
# ax.axvline(t_uni, label = f'z={z}', c='k', alpha = 0.2)

handles = [Line2D([0], [0], label = fr'$\rm instantaneous\ burst$' , color='k', lw=1, ls='--')]
handles += [Line2D([0], [0], label = fr'$\rm constant\ SF$' , color='k', lw=1, ls='-')]
handles += [Line2D([0], [0], label = fr'$\rm \tau_{{V}}={10**log10tau_V:.1f}$' , color=cm.magma(j/4), lw=1) for j,log10tau_V in enumerate([-5., -1.0, -0.3, 0.0])]
handles += [Line2D([0], [0], label = fr'$\rm f_{{esc}}=1$' , color='0.5', lw=1, ls='-')]

ax.legend(handles=handles, fontsize=7, labelspacing = 0.1)



ax.set_ylim([-1., 2])
ax.set_xlim([6., 9.0])

ax.set_xlabel(r'$\rm log_{10}(t_{SF}/yr)$')
ax.set_ylabel(r'$\rm -2.5\times\log_{10}(L_{4200}/L_{3500})$')

fig.savefig(f'figs/BB.pdf')
fig.clf()
