# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import random
import json

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from ..chapter_4.vectors import vector_mean, squared_distance, distance


class KMeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k  # number of clusters
        self.means = None  # means of clusters

    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):

        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            # Find new assignments
            new_assignments = list(map(self.classify, inputs))

            # If no assignments have changed, we're done.
            if assignments == new_assignments:
                return

            # Otherwise keep the new assignments,
            assignments = new_assignments

            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a == i]
                # avoid divide-by-zero if i_points is empty
                if i_points:
                    self.means[i] = vector_mean(i_points)


def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)

    return sum(squared_distance(input, means[cluster])
               for input, cluster in zip(inputs, assignments))


def recolor_image(input_file, k=5):
    img = mpimg.imread(input_file)
    pixels = [pixel for row in img for pixel in row]
    clusterer = KMeans(k)
    clusterer.train(pixels)  # this might take a while

    def recolor(pixel):
        cluster = clusterer.classify(pixel)  # index of the closest cluster
        return clusterer.means[cluster]  # mean of the closest cluster

    new_img = [[recolor(pixel) for pixel in row]
               for row in img]

    plt.imshow(new_img)
    plt.axis('off')
    plt.show()


def is_leaf(cluster):
    """a cluster is a leaf if it has length 1"""
    return len(cluster) == 1


def get_children(cluster):
    """returns the two children of this cluster if it's a merged cluster;
    raises an exception if this is a leaf cluster"""
    if is_leaf(cluster):
        raise TypeError("a leaf cluster has no children")
    return cluster[1]


def get_values(cluster):
    """returns the value in this cluster (if it's a leaf cluster)
    or all the values in the leaf clusters below it (if it's not)"""
    if is_leaf(cluster):
        return cluster  # is already a 1-tuple containing value
    else:
        return [value
                for child in get_children(cluster)
                for value in get_values(child)]


def cluster_distance(cluster1, cluster2, distance_agg=min):
    """compute all the pairwise distances between cluster1 and cluster2
    and apply _distance_agg_ to the resulting list"""
    return distance_agg([distance(input1, input2)
                         for input1 in get_values(cluster1)
                         for input2 in get_values(cluster2)])


def get_merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0]  # merge_order is first element of 2-tuple


def bottom_up_cluster(inputs, distance_agg=min):
    # start with every input a leaf cluster / 1-tuple
    clusters = [(input_,) for input_ in inputs]

    # as long as we have more than one cluster left...
    while len(clusters) > 1:
        # find the two closest clusters
        c1, c2 = min([(cluster1, cluster2)
                      for i, cluster1 in enumerate(clusters)
                      for cluster2 in clusters[:i]],
                     key=lambda p: cluster_distance(p[0], p[1], distance_agg))

        # remove them from the list of clusters
        clusters = [c for c in clusters if c not in [c1, c2]]

        # merge them, using merge_order = # of clusters left
        merged_cluster = (len(clusters), [c1, c2])

        # and add their merge
        clusters.append(merged_cluster)

    # when there's only one cluster left, return it
    return clusters[0]


def generate_clusters(base_cluster, num_clusters):
    # start with a list with just the base cluster
    clusters = [base_cluster]
    # as long as we don't have enough clusters yet...
    while len(clusters) < num_clusters:
        # choose the last-merged of our clusters
        next_cluster = min(clusters, key=get_merge_order)
        # remove it from the list
        clusters = [c for c in clusters if c != next_cluster]
        # and add its children to the list (i.e., unmerge it)
        clusters.extend(get_children(next_cluster))

    # once we have enough clusters...
    return clusters


if __name__ == "__main__":
    inputs = [[-14, -5], [13, 13], [20, 23], [-19, -11], [-9, -16], [21, 27],
              [-49, 15], [26, 13], [-46, 5], [-34, -1], [11, 15], [-49, 0],
              [-22, -16], [19, 28], [-12, -8], [-13, -19], [-41, 8], [-11, -6],
              [-25, -9], [-18, -3]]

    random.seed(0)  # so you get the same results as me
    clusterer = KMeans(3)
    clusterer.train(inputs)
    print("3-means:")
    print(clusterer.means)
    print()

    random.seed(0)
    clusterer = KMeans(2)
    clusterer.train(inputs)
    print("2-means:")
    print(clusterer.means)
    print()

    random.seed(0)
    clusterer = KMeans(4)
    clusterer.train(inputs)
    print("4-means:")
    print(clusterer.means)
    print()

    # now plot from 1 up to len(inputs) clusters
    ks = range(1, len(inputs) + 1)

    errors = [squared_clustering_errors(inputs, k) for k in ks]
    plt.plot(ks, errors)
    plt.xticks(ks)
    plt.xlabel("k")
    plt.ylabel("total squared error")
    plt.title("Total Error vs. # of Clusters")
    # plt.show()

    directory = "/home/hermogenes/Downloads/"
    path_image = directory + "acoes.png"
    # recolor_image(path_image, 8)

    base_cluster = bottom_up_cluster(inputs)
    # print(json.dumps(base_cluster))

    print()
    print("three clusters, min:")
    for cluster in generate_clusters(base_cluster, 3):
        print(get_values(cluster))

    print()
    print("three clusters, max:")
    base_cluster = bottom_up_cluster(inputs, max)
    for cluster in generate_clusters(base_cluster, 3):
        print(get_values(cluster))

    three_clusters = [get_values(cluster)
                      for cluster in generate_clusters(base_cluster, 3)]

    for i, cluster, marker, color in zip([1, 2, 3],
                                         three_clusters,
                                         ['D', 'o', '*'],
                                         ['r', 'g', 'b']):
        xs, ys = zip(*cluster)  # magic unzipping trick
    plt.scatter(xs, ys, color=color, marker=marker)
    # put a number at the mean of the cluster
    x, y = vector_mean(cluster)
    plt.plot(x, y, marker='$' + str(i) + '$', color='black')
    plt.title("User Locations -- 3 Bottom-Up Clusters, Min")
    plt.xlabel("blocks east of city center")
    plt.ylabel("blocks north of city center")
    plt.show()