import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

twiss_df_b2 = pd.read_parquet('../twiss_b2_for_b4check_seq_lhcb2.parquet')
twiss_df_b4 = pd.read_parquet('../twiss_b4_for_b4check_seq_lhcb2.parquet')


plt.close('all')
matplotlib.rc('font', size=14)

# %%
fig = plt.figure(1, figsize=(6.4*1.6, 4.8*1.5))
axbetx = fig.add_subplot(2,2,1)
axbetx.plot(twiss_df_b4['s'][-1]-twiss_df_b4['s'],twiss_df_b4['betx'],
        'b', lw=2)
axbetx.plot(twiss_df_b2['s'], twiss_df_b2['betx'],'--g', lw=2)
axbetx.set_xlabel('s [m]')
axbetx.set_ylabel(r'$\beta_x$ [m]')
axbetx.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
axbetx.ticklabel_format(style='sci', scilimits=(0, 0), axis='x')

# %%
axbety = fig.add_subplot(2,2,2, sharex=axbetx, sharey=axbetx)
axbety.plot(twiss_df_b4['s'][-1]-twiss_df_b4['s'],twiss_df_b4['bety'],
        'b', label='b4', lw=2)
axbety.plot(twiss_df_b2['s'], twiss_df_b2['bety'],'--g', lw=2, label='b2')
axbety.set_xlabel('s [m]')
axbety.set_ylabel(r'$\beta_y$ [m]')
axbety.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
axbety.ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
axbety.legend()
# %%

axcox = fig.add_subplot(2,2,3, sharex=axbetx)
axcox.plot(twiss_df_b4['s'][-1]-twiss_df_b4['s'],-twiss_df_b4['x'],'b', lw=2)
axcox.plot(twiss_df_b2['s'], twiss_df_b2['x'], '--g', lw=2)
axcox.set_xlabel('s [m]')
axcox.set_ylabel('x [m]')
axcox.ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
axcox.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
#plt.xlim(5500,7500)
# %%
axcoy = fig.add_subplot(2,2,4, sharex=axbetx, sharey=axcox)
axcoy.plot(twiss_df_b4['s'][-1]-twiss_df_b4['s'],twiss_df_b4['y'],'b', lw=2)
axcoy.plot(twiss_df_b2['s'], twiss_df_b2['y'], '--g', lw=2)
axcoy.set_xlabel('s [m]')
axcoy.set_ylabel('y [m]')
axcoy.ticklabel_format(style='sci', scilimits=(0, 0), axis='x')
axcoy.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')

fig.subplots_adjust(left=.1, bottom=.08, right=.94, top=.95,
        wspace=.3, hspace=.24)
plt.show()
