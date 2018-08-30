import matplotlib.pyplot as plt
import numpy as np
import copy

points=[]

#x=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]

#y=[0.500536494,0.479190903,0.551950574,0.644833703,0.839210862,1.409537201,2.116133364,2.745857983,3.088957947,2.782280943,2.108415582,1.334671344,0.810013498,0.663736266,0.500823623,0.529501897,0.529607027,0.539474117,0.448612051,0.51934221,0.436796141]
x=[0,430,665,930,1155]

y=[450,400,300,150,0]

#x=[1,3,6,10]
#y=[2,5,7,6]


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

plt.show()
