
# coding: utf-8

# In[1]:


import json
import sys, operator


# ## Task 1

# In[2]:


GROUND_TRUTH_FILE = './GroundTruth_File'
SENSING_MATRIX_FILE = './SCMatrix_Test1'
# SENSING_MATRIX_FILE = './SCMatrix_Test2'
# SENSING_MATRIX_FILE = './SCMatrix_Test3'


# In[3]:


def readSensingMatrix(filename):
    matrix = {}
    f = open(filename, 'r')
    for line in f:
        source_id, measured_variable_id = [int(x) for x in line.split(',')]
        if source_id not in matrix:
            matrix[source_id] = {}
        matrix[source_id][measured_variable_id] = 1
    f.close()
    return matrix

# In[5]:


# ## Task 2

# In[6]:


TWEETS_FILE = './Tweets.txt'
CLUSTERS_FILE = './Cluster_Results.txt'
SENSING_MATRIX_FILE = './SCMatrix_Task2'
OUTPUT_PROBS_FILE = './Task2_Probs.txt'


# In[8]:


from Task1 import TruthDiscovery
from Task2 import loadJsonTwitter, loadClusterResults, writeSensMatrixFile

tweets = loadJsonTwitter(TWEETS_FILE)
clusters = loadClusterResults(CLUSTERS_FILE)
writeSensMatrixFile(tweets, clusters, SENSING_MATRIX_FILE)

matrix = readSensingMatrix(SENSING_MATRIX_FILE)

td = TruthDiscovery(matrix)
td.mle()
td.writeProbs(OUTPUT_PROBS_FILE)
