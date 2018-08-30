import matplotlib.pyplot as plt
import numpy as np
import copy
import math
points=[]
error=[]
def spline(points):
    x = list(map(lambda p: float(p[0]), points))
    y = list(map(lambda p: float(p[1]), points))
    N = len(points) - 1
    h = {}
    l = {}
    delta = {}
    _lambda = {}
    c = {}
    c[0] = 0
    c[N] = 0
    d = {}
    b = {}
    r = []
    for i in range(1, N+1):
        h[i] = x[i] - x[i-1]
        l[i] = (y[i] - y[i-1]) / h[i]
    delta[1] = - h[2]/(2 * (h[1] + h[2]))
    _lambda[1] = 1.5 * (l[2] - l[1]) / (h[1] + h[2])
    for i in range(3, N+1):
        delta[i-1] = - h[i] / (2 *h[i-1] + 2 * h[i] + h[i-1] * delta[i-2])
        _lambda[i-1] = (3 * l[i] - 3 * l[i-1] - h[i-1] * _lambda[i-2]) / \
                       (2 * h[i-1] + 2 * h[i] + h[i-1] * delta[i-2])
    for i in range(N, 1, -1):
        c[i-1] = delta[i-1] * c[i] + _lambda[i-1]
        #array_c.insert(0,c[i-1])
    for i in range(1, N+1):
        d[i] = (c[i] - c[i-1]) / (3 * h[i])
        b[i] = l[i] + (2 * c[i] * h[i] + h[i] * c[i-1]) / 3
    return  b, c, d


#созданние масивов (для интерполяции)
n=8
N=list(range(1,n+1))
x=list(map(lambda i: 2*np.pi/(n-1)*(i-1), N))
y=list(map(lambda i: 4*math.exp(-0.5*(4-i)**2)+0.5, x))


#созданние масивов (для нахождения ошибки)
m=1000
M=list(range(1,m+1))
X=list(map(lambda i: 2*np.pi/(m-1)*(i-1), M))
Y=list(map(lambda i: 4*math.exp(-0.5*(4-i)**2)+0.5, X))



#для работы с графиками
fig = plt.figure()
print (fig.axes)
print (type(fig))

for i in range(len(x)):
    plt.scatter(x[i],y[i])


#преобразование массивов
for i in range(len(x)):
    points.append([x[i],y[i]])

#вычисление коэфиициентов
b, c, d=spline(points)

N = len(points)

#вывод каждого сплайна по циклу
for i in range(1,N):
    xi_1=x[i-1]
    xi=x[i]

    ai=y[i]
    bi=b[i]
    ci=c[i]
    di=d[i]

    #T=np.arange(xi_1,xi+0.1,0.1)
    T=np.arange(xi_1,xi+0.1,0.1)
    T2 = copy.deepcopy(T)
    for l in range(len(T)):
        T2[l]=T2[l]-xi
    y1=ai+bi*T2+ci*T2**2+di*T2**3
    plt.plot(T, y1)

for i in range(1,N):
    xi_1=x[i-1]
    xi=x[i]

    ai=y[i]
    bi=b[i]
    ci=c[i]
    di=d[i]

    for j, xj in enumerate(X):
        #print(j, xj)
        if xj<=xi and xj>xi_1:
            t=xj-xi
            y1=ai+bi*t+ci*t**2+di*t**3
            e=Y[j]-y1
            error.append(e)

print(error)

#for i in range(len(X)):
#    plt.scatter(X[i],error[i])



plt.show()
