import json
import sys

import mpld3
from mpld3 import plugins
from numpy import cos, sin
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import pp.pptools as pptools

plt.switch_backend('agg')


def func(t, x, data):
    v = []
    for i in np.arange(len(data['func'])):
        v.append(eval(data['func'][i]))
    return v


def main(jsonData):
    fig = plt.figure()
    data = jsonData
    state0 = data['x0']
    tick = data['tick']
    fperiod = 2.0 * np.pi
    duration = fperiod * data['period']
    tspan = np.arange(0, duration, tick)
    i = 0
    while i < 50:
        state = solve_ivp(func, (0, duration), state0,
                          t_eval=tspan,
                          rtol=1e-6,
                          # method = 'DOP853',
                          method='RK45', args=(data,))
        plt.plot(state.y[0, :], state.y[1, :],
                 linewidth=1, color=(0, 0, 0),
                 ls="-", alpha=data['alpha'])
        plt.plot(state.y[0, -1], state.y[1, -1], 'o',
                 markersize=2, color="red", alpha=data['alpha'])
        state0 = data['x0'] = state.y[:, -1]
        i += 1
    plugins.connect(fig, plugins.MousePosition(fontsize=14))
    html = mpld3.fig_to_html(fig)
    # mpld3.save_html(fig,'111.html')
    plt.close()
    # plt.show()
    return html
