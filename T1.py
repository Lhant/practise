from sympy import ln, exp, sin
from sympy.plotting import plot
import sympy as sp


def returnDiff(fx: str):
    y = sp.factor(fx)
    return y.diff('x')


def foo(num):
    try:
        float(num)
        return True
    except:
        # print('根は複数')
        return False


def balancePoint(fx: str):
    # x = sp.symbols("x")
    fx = sp.factor(fx)
    fx1 = sp.factor(returnDiff(fx))
    xList = []
    xList = sp.solve(fx, x)
    returnList = []
    for item in xList:
        # 判断非复数
        if foo(item):
            if fx1.subs(x, item) < 0:
                returnList.append('x：' + str(item) + 'は平衡点')
            else:
                returnList.append('x：' + str(item) + 'は平衡点じゃない')
    return returnList


# x·=x^2-1的の平衡点を求める
x = sp.symbols("x")
# t = x ** 2 + 1
# t = (x - 4) * (x - 3) * (x - 2) * (x - 1)
# t = ln(x)
# t = exp(x)-2000
t = sin(x)
p = plot(t, show=False)
p.ylabel = 'x·'
# p.title = 'x·=x^3+1'
p[0].line_color = 'r'
p.show()
print(balancePoint(t))
