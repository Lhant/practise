from io import BytesIO
import function.myFunction as myFun
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from numpy.core import size
from scipy.integrate import odeint


# dx/dt=ax-x**2 ,dy/dt=-y

def func(s, t, a):
    x, y = s
    return [a * x - x ** 2, -y]


def funImg(x, y, a):
    buf = BytesIO()
    # plt.subplot(1, 2, 1)
    y0 = [x, y]
    t = np.linspace(0, 10, 300)
    sol = odeint(func, y0, t, args=(a,))
    plt.plot(sol[:, 0], sol[:, 1], 'b', linestyle='-', marker='')  # yについてplot
    for i in range(size(sol[:, 0]) - 1):
        plt.quiver(sol[:, 0][i], sol[:, 1][i],
                   sol[:, 0][i + 1] - sol[:, 0][i], sol[:, 1][i + 1] - sol[:, 1][i], color='y')
    plt.legend(loc='best')  # レジェンドを付ける
    plt.xlabel('t')
    plt.grid()  # 格子を付ける
    # plt.show()
    plt.savefig(buf)
    imd = myFun.saveBase64Img(buf)
    return imd


if __name__ == '__main__':
    funImg(1, 1, 2)
