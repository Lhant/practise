import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins, utils

x,y = np.random.rand(2,10)
fig, ax = plt.subplots()
ax.scatter(x,y,s=10,c='orange')

plugins.connect(fig, plugins.MousePosition())
mpld3.save_html(fig,'111.html')
mpld3.show()