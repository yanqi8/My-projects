import numpy as np

import os
os.environ['SPARK_HOME'] =".../spark-2.2.0-bin-hadoop2.7"
import findspark
findspark.init()

import pyspark
sc = pyspark.SparkContext()

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()


# matrix multiplication for sparse matrix
def randSparse(n, k):
    entries = []
    for i in range(k):
        entries.append((np.random.randint(n), np.random.randint(n), np.random.rand(1)[0]))

    return entries

# 2 sparse matrix
n = 100
k = 300
A = sc.parallelize(randSparse(n,k))
B = sc.parallelize(randSparse(n,k))

# vector for later check
v = np.random.randn(n)
V = sc.parallelize(zip(range(n), v))

def mat_vec(Mat,X):
    Mat_cols = Mat.map(lambda x : (x[1], (x[0], x[2])))
    XMat = Mat_cols.join(X)
    XMult = XMat.map(lambda x : (x[1][0][0], x[1][0][1] * x[1][1]))
    Y = XMult.reduceByKey(lambda x , y : x + y)

    return Y

def RDD_to_numpy(Y):
    y = np.zeros((n))
    for idx, val in Y.collect():
        y[idx] = val
    return y


def mat_mul(A, B):
    ##no forloops allowed. Get a zero if use a for loop. no collect calls allowed get zero if use a collect call
    A_cols = A.map(lambda x: (x[1], (x[0], x[2])))
    B_temp = B.map(lambda x: (x[0], (x[1], x[2])))
    AB = A_cols.join(B_temp)
    Mult = AB.map(lambda x: ((x[1][0][0], x[1][1][0]), x[1][0][1] * x[1][1][1]))
    Y = Mult.reduceByKey(lambda x, y: x + y)

    ABMul = Y.map(lambda x: (x[0][0], x[0][1], x[1]))

    return ABMul

# test and check
C = mat_mul(A,B)
ans1 = RDD_to_numpy(mat_vec(A, mat_vec(B, V)))
ans2 = RDD_to_numpy(mat_vec(C, V))
print 'this should be small: ', np.linalg.norm(ans1-ans2)