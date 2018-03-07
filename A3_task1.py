
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


# In[4]:


matrix = readSensingMatrix(SENSING_MATRIX_FILE)


# In[5]:


from Task1 import TruthDiscovery

td = TruthDiscovery(matrix)
td.mle()
td.verify(GROUND_TRUTH_FILE)
