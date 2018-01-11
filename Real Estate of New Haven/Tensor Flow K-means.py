import gzip
import hashlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf
from itertools import cycle


# get data
dat = pd.read_csv('finaldf_all.csv')
dat2 = dat.loc[:,['totval','neighborhood','sqft','latitude','longitude']]
ind = list(np.where(dat2['sqft']==0)[0])
dat2.loc[ind, 'sqft'] = np.nan
dat3 = dat2.dropna(axis=0, how='any')


# Total number of points in the dataset
number_of_points = dat3.shape[0]
# The dimension of each point.
dimension = 2

number_of_clusters = 40 #New Haven is made up of approximately 40 distinct neighborhoods

true_assignments = np.array(dat3.loc[:,'neighborhood'])

points_values = np.array(dat3.loc[:,['latitude','longitude']])
# The maximum number of iterations in the k-means algorithm
maximum_number_of_steps = 1000

points = tf.constant(points_values,tf.float32)
centroids = tf.Variable(tf.slice(tf.random_shuffle(points), [0, 0], [number_of_clusters, -1]))
points_expanded = tf.expand_dims(points, 0)
centroids_expanded = tf.expand_dims(centroids, 1)

# compute the distances and closest_center
distances = tf.reduce_sum(tf.square(tf.subtract(points_expanded, centroids_expanded)), 2)
assignments = tf.argmin(distances, 0)


# For each cluster c, compute the mean of all points currently assigned to the cluster c
means = []
for c in xrange(number_of_clusters):
    means.append(tf.reduce_mean(
      tf.gather(points,
                tf.reshape(
                  tf.where(
                    tf.equal(assignments, c)
                  ),[1,-1])
               ),reduction_indices=[1]))
new_centroids = tf.concat(means, 0)

# placeholder
old_centroids = tf.Variable(tf.random_normal([number_of_clusters,dimension]), tf.float32)
assign_old = tf.assign(old_centroids, centroids)
update_centroids = tf.assign(centroids, new_centroids)

# compute the change of centers
d_change = tf.reduce_sum(tf.square(tf.subtract(old_centroids, centroids)),1)


# Run Tensor print centers
done = False
with tf.Session() as sess:
    tf.global_variables_initializer().run()
    while not(done):
        [_, _, centers, center_change, points_values, ass] = \
        sess.run([update_centroids, assign_old, centroids,d_change, points, assignments])
        if (np.linalg.norm(center_change) < 10**(-6)):
            done = True

    print "centroids" + "\n", centers
    print "center_change" + "\n", center_change


# original zone in the chaos data
plt.scatter(points_values[:, 1], points_values[:, 0], c = pd.factorize(true_assignments)[0], alpha=0.5)
plt.show()

# k-means zone
plt.scatter(points_values[:, 1], points_values[:, 0], c = ass, alpha=0.5)
plt.show()
