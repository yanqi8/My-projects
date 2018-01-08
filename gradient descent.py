import hashlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# toy gradient descent project

# sigmoid function
def sigmoid(z):
    return 1/(1+np.exp(-z))

np.random.seed(1)
n = 8
d = 4
A = np.random.randn(n,d)
b = np.round(np.random.rand(n,1))

def f(x):
    ad=0
    for i in range(0,n) :
        temp = (sigmoid(np.dot(A[i,],x))-b[i])**2
        ad = ad+temp
    return ad

def sigmoid_deriv(z):
    return np.exp(-z)/(1+np.exp(-z))**2

def grad_f(x):
    ad_g=0
    for i in range(0,n) :
        temp_g = 2*(sigmoid(np.dot(A[i,],x))-b[i])*sigmoid_deriv(np.dot(A[i,],x))*A[i,]
        ad_g = ad_g+ temp_g
    return ad_g


hash_object = hashlib.md5('yq76')
hex_hash = hash_object.hexdigest()
seed = int(hex_hash[0:4],16)
print "seed : ", seed
np.random.seed(int(hex_hash[0:4],16))

n = 30
d = 10

A = np.random.randn(n,d)
b = np.round(np.random.rand(n,1))

x0 = np.random.randn(d)


def grad_descent(x0, f, g, tol=10 ** (-6), max_iters=10 ** 5):
    f0 = f(x0)
    g0 = g(x0)

    step_size = 50
    iters = 0

    while ((np.linalg.norm(g0) > tol) & (step_size > tol) & (iters < max_iters)):
        xnew = x0 - step_size * g0
        fnew = f(xnew)
        iters += 1

        if (fnew < f0):
            f0 = fnew
            x0 = xnew
            g0 = g(x0)
        else:
            step_size = step_size / 2

    print "function value:", f0
    print "number iterations:", iters
    print step_size

    return x0


def grad_ascent(x0, f, g, tol=10 ** (-6), max_iters=10 ** 5):
    f0 = f(x0)
    g0 = g(x0)

    step_size = 30
    iters = 0

    while ((np.linalg.norm(g0) > tol) & (step_size > tol) & (iters < max_iters)):
        xnew = x0 + step_size * g0
        fnew = f(xnew)
        iters += 1

        if (fnew > f0):
            f0 = fnew
            x0 = xnew
            g0 = g(x0)
        else:
            step_size = step_size / 2

    print "function value:", f0
    print "number iterations:", iters
    print step_size

    return x0


xm = grad_ascent(x0, f, grad_f) # reach local max f(x) value approximately at 21.99
np.linalg.norm(grad_f(xm)) #check for norm


def grad_ascent2(x0, f, g, tol=10 ** (-7), max_iters=10 ** 4):
    f0 = f(x0)
    g0 = g(x0)

    step_size = 30
    iters = 0

    while ((np.linalg.norm(g0) > tol) & (step_size > tol) & (iters < max_iters)):
        xnew = x0 + step_size * g0
        fnew = f(xnew)
        iters += 1

        if (fnew > f0):
            f0 = fnew
            x0 = xnew
            g0 = g(x0)
        else:
            step_size = step_size / 2

    print "function value:", f0
    print "number iterations:", iters
    print step_size

    return x0


xm2 = grad_ascent2(xm, f, grad_f) # find a wider area of local maxima
np.linalg.norm(grad_f(xm2)) # check for norm

d=xm2-xm
x1=xm2+2*d+50
x2=xm2-2*d-80

# final test
if np.linalg.norm(grad_f(x1)) < 1e-6:
    print "gradient at x1 is small!"
else:
    print "x1 failed gradient test"

if np.linalg.norm(grad_f(x2)) < 1e-6:
    print "gradient at x2 is small!"
else:
    print "x2 failed gradient test"

if f((x1+x2)/2) - max(f(x1),f(x2)) > 0.1:
    print "The value between is significantly higher."
else:
    print "The value between is not large enough. Find different points."


