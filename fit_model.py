import numpy as np
import scipy.optimize

import matplotlib.pyplot as plt

## fit simple model function
## y(t) = y1 for t < t1
## y(t) = y1 + a2 * (t-t1) for t1 < t < t2
## y(t) = y1 + a2 * (t2-t1) for t2 < t

def model_function(p, t):
    y1 = p[0]
    t1 = p[1]
    a2 = p[2]
    t2 = p[3]

    res = y1 + a2 * (t-t1)
    res[t<t1] = y1
    res[t>t2] = y1 + a2 * (t2-t1)

    return res

def diff_function(p, data_t, data_p):
    model_p = model_function(p, data_t)

    res = np.sum((model_p - data_p)**2)

    if p[0] < 0: res *= 2
    if p[1] < 0: res *= 2

    return res

data = np.loadtxt("output2/results.csv", delimiter=';')

t_max = data[-1,0]
p_max = data[-1,1]

data_t = data[:,0] / t_max
data_p = data[:,1] / p_max

p0 = np.array([0, 0.1, 1./(0.8), 0.9])

result = scipy.optimize.minimize(diff_function, p0, (data_t, data_p),
                                 method = 'Nelder-Mead',
                                 options={'maxiter':1000})

p = result.x

data_t *= t_max
data_p *= p_max

p[0] *= p_max
p[1] *= t_max
p[2] *= (p_max / t_max)
p[3] *= t_max

print result

plt.plot(data_t, data_p, label='experiment')
plt.plot(data_t, model_function(p, data_t), label='fit')
plt.title("y1 = {:8.2e}; t1 = {:8.2e}; a2 = {:8.2e}; t2 = {:8.2e}".format(p[0], p[1], p[2], p[3]))
plt.xlabel("time [s]")
plt.ylabel("position [cm]")
plt.legend()
plt.savefig("output2/fit.pdf")
plt.show()