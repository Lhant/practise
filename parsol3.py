import sys, json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy import linalg
from numpy import cos
from numpy.linalg import solve, det


def getDict():
    fp = Path('in3.json').open()
    Dict = json.load(fp)
    fp.close()
    return Dict


def func(t, x, data):
    p = -3.0 * x[0] * x[0]
    k = data['params'][0]
    B0 = data['params'][1]
    B = data['params'][2]
    Q = -6 * x[0]
    listL = [x[1], -k * x[1] - x[0] ** 3 + B0 + B * cos(t),
             x[3], p * x[2] - k * x[3],
             x[5], p * x[4] - k * x[5],
             x[7], p * x[6] - k * x[7] + cos(t),
             x[9], p * x[8] - k * x[9] + Q * x[2] * x[2],
             x[11], p * x[10] - k * x[11] + Q * x[2] * x[4],
             x[13], p * x[12] - k * x[13] + Q * x[4] * x[4],
             x[15], p * x[14] - k * x[15] + Q * x[2] * x[6],
             x[17], p * x[16] - k * x[17] + Q * x[4] * x[6]]
    listAll = np.array([])
    for item in listL:
        listAll = np.append(listAll, np.array(item).flatten())
    return listAll


if __name__ == '__main__':
    data = getDict()
    fperiod = 2 * np.pi
    duration = data['period'] * fperiod
    x0 = data['x0']
    i = 0
    while True:
        print("Begin with k=%f,B0=%f,B=%f" % tuple(data['params']))
        print("Begin with x=", x0)
        prev = x0
        x00 = np.append(x0, [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        x = solve_ivp(func, (0, duration), x00,
                      # method = 'DOP853',
                      method='RK45',
                      rtol=1e-8,
                      args=(data,))  # pass a singleton
        vec = x.y[:, -1]
        print("现在的函数值是：", vec)
        a = -(-1) * (vec[8] + vec[11]) + vec[8] * vec[5] + vec[2] * vec[11] - \
            vec[10] * vec[3] - vec[4] * vec[9]
        b = -(-1) * (vec[10] + vec[13]) + vec[10] * vec[5] + vec[2] * vec[13] - \
            vec[12] * vec[3] - vec[4] * vec[11]
        c = -(-1) * (vec[14] + vec[17]) + vec[14] * vec[5] + vec[2] * vec[17] - \
            vec[16] * vec[3] - vec[4] * vec[15]

        A = np.array([[vec[2] - 1, vec[4], vec[6]], [vec[3], vec[5] - 1, vec[7]], [a, b, c]])
        print(A, det(A))
        dTdx = np.array([[vec[2], vec[4]], [vec[3], vec[5]]])
        f3 = dTdx - (-1) * np.eye(2)
        print("Jacobian 是", f3)
        print("现在的解是", [x0[0] - vec[0], x0[1] - vec[1], -det(f3)])
        h = solve(A, np.array([vec[0] - x0[0], vec[1] - x0[1], det(f3)]))
        print("步长，", h)
        x0 = x0 - h[0:2]
        data['params'][2] = data['params'][2] - h[2]
        print(x0, data['params'][2])
        i += 1
        if abs(h[2]) < 1e-8:
            print('--------------------End--------------------')
            print('i:%d' % i)
            print("k=%f,B0=%f,B=%f" % tuple(data['params']))
            print("x=", x0)
            break
