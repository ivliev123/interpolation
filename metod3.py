import matplotlib.pyplot as plt
import numpy as np
import copy

points=[]

#x=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]

#y=[0.500536494,0.479190903,0.551950574,0.644833703,0.839210862,1.409537201,2.116133364,2.745857983,3.088957947,2.782280943,2.108415582,1.334671344,0.810013498,0.663736266,0.500823623,0.529501897,0.529607027,0.539474117,0.448612051,0.51934221,0.436796141]

q1=[430,665,930,1155]
p1=[400,300,150,0]
n1=[2675,2350,1905,1550]

q2=[305,510,795,1060]
p2=[203,177,112,0]
n2=[1935,1825,1660,1470]

q3=[255,375,610,830]
p3=[109,96,65,0]
n3=[1405,1345,1260,1140]

q4=[125,215,345,475]
p4=[34,31,21,0]
n4=[800,770,730,685]

q=[q1,q2,q3,q4]
p=[p1,p2,p3,p4]
n=[n1,n2,n3,n4]

N_array=[]
Q_array=[]
N_obr=1000

U=[7.5,6.86,4.58,2.26]
U_new=[]
#x=[1,3,6,10]
#y=[2,5,7,6]

def get_points(x,y):
    #преобразование массивов
    points=[]
    yx=[]
    for i in range(len(x)):
        points.append([])
        for k in range(len(x[i])):
            points[i].append([x[i][k],y[i][k]])
    #вычисление коэфиициентов
    for i in range(len(points)):
        a, b, c, d=spline(points[i])
        yx.append([a, b, c, d])
    return yx

def diapazon(n,N,namber):
    for i in range(len(n[namber])-1):
        if N<=n[namber][i] and N>=n[namber][i+1] or N>=n[namber][i] and N<=n[namber][i+1]:
            return i,i+1

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
    a = {}
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
        a[i] = y[i]
    return a, b, c, d

#номер кривой, массив семейства кривых по оси x, массив коэфициентов интерполяции, значение X
def find_points(namber,x_all,x_y,x_val):
    t1,t2=diapazon(x_all,x_val,namber)

    x=x_all[namber]
    xi_1=x[t1]
    xi=x[t2]

    ai=x_y[namber][0][t2]
    bi=x_y[namber][1][t2]
    ci=x_y[namber][2][t2]
    di=x_y[namber][3][t2]

    Y=ai+bi*(x_val-xi)+ci*(x_val-xi)**2+di*(x_val-xi)**3
    return Y


def figure(x_y,x_all):
    for i in range(len(x_y)):
        #a, b, c, d=spline(points[i])
        x = x_all[i]
        for k in range(1,len(x)):
            xi_1=x[k-1]
            xi=x[k]

            ai=x_y[i][0][k]
            bi=x_y[i][1][k]
            ci=x_y[i][2][k]
            di=x_y[i][3][k]
            #print(ai,bi,ci,di)

            #T=np.arange(xi_1,xi+0.1,0.1)
            T=np.arange(xi_1,xi+0.1,-0.1)
            T2 = copy.deepcopy(T)
            for l in range(len(T)):
                T2[l]=T2[l]-xi
            y=ai+bi*T2+ci*T2**2+di*T2**3
            plt.plot(T, y)

#для работы с графиками
fig = plt.figure()

#for i in range(len(n)):
    #plt.scatter(n[i],p[i])

#for i in range(len(n)):
#    plt.scatter(n[i],q[i])

n_p=get_points(n,p)
p_n=get_points(p,n)
n_q=get_points(n,q)
q_p=get_points(q,p)

figure(p_n,p)

#поиск статистического давления, указав кривую и условно считав обороты
namber=3
N=740
P=find_points(namber,n,n_p,N)


for i in range(len(p_n)):
    if p[i][0]>P:
        N = find_points(i,p,p_n,P)

        plt.scatter(P,N)


fig.savefig(str(namber)+'_'+str(N)+'.png')
plt.show()
