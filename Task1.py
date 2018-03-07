import json
import sys, operator

class TruthDiscovery():
    
    def __init__(self, matrix):
        
        self.matrix = matrix
        self.num_sources = len(matrix)
        self.num_measured_variables = self.calcTotNumMeasuredVariables()
        
        self.a = self.initAi()
        self.b = self.initBi()
        
        self.d = 0.5
        
        self.Z = dict.fromkeys(range(1,self.num_measured_variables+2))
        self.H = dict.fromkeys(range(1,self.num_measured_variables+2))
        self.E = dict.fromkeys(self.matrix.keys()) 

    def numMeasuredVariables(self, source_id):
        return len(self.matrix[source_id])

    def calcTotNumMeasuredVariables(self):
        max_var = 0
        for source_id in self.matrix:
            sorted_measured_variables = sorted(self.matrix[source_id].keys())
            max_var = max(max_var, sorted_measured_variables[-1])
        return max_var-1

    def calcSi(self, i):
        return len(self.matrix[i]) / float(self.num_measured_variables)

    def initAi(self):
        a = {}
        for i in self.matrix.keys():
            a[i] = self.calcSi(i)
        return a

    def initBi(self):
        b = {}
        for i in self.matrix.keys():
            b[i] = self.calcSi(i) * 0.5
        return b

    def calcNextAi(self, s):
        numerator = sum([self.Z[j] for j in self.Z if j in self.matrix[s]])
        denominator = sum(self.Z.values())
        return numerator / float(denominator)

    def calcNextBi(self, s):
        Ki = self.numMeasuredVariables(s)
        N = self.num_measured_variables
        numerator = sum([self.Z[j] for j in self.Z if j in self.matrix[s]])
        denominator = sum(self.Z.values())
        return (Ki - numerator) / float(N - denominator)

    def calcNextDi(self, s):
        numerator = sum(self.Z.values())
        return numerator / float(self.num_measured_variables)

    def calcA(self, j):
        PI = 1
        for i in self.matrix:
            if j in self.matrix[i]:
                PI *= self.a[i]
            else:
                PI *= (1-self.a[i])
        return PI

    def calcB(self, j):
        PI = 1
        for i in self.matrix:
            if j in self.matrix[i]:
                PI *= self.b[i]
            else:
                PI *= (1-self.b[i])
        return PI

    def calcZ(self, j):
        numerator = self.calcA(j) * self.d
        denominator = self.calcA(j) * self.d + self.calcB(j) * (1 - self.d)
        return numerator / float(denominator)

    def calcSourceReliability(self, s):
        return self.a[s] * self.d / float(self.calcSi(s))

    def expectationMaximization(self):
        t = 0
        while t < 20:

            for j in self.Z:
                self.Z[j] = self.calcZ(j)

            for i in self.matrix:
                self.a[i] = self.calcNextAi(i)
                self.b[i] = self.calcNextBi(i)
                self.d = self.calcNextDi(i)
            t += 1

        for j in self.Z:
            if self.Z[j] >= 0.5:
                self.H[j] = 1
            else:
                self.H[j] = 0

        for i in self.matrix:
            self.E[i] = self.calcSourceReliability(i)

    def verifyTruth(self, ground_file):
        truth_dict = {}
        f = open(ground_file)
        for line in f:
            measured_variable_id, correctness_indicator = line.split(',')
            truth_dict[int(measured_variable_id)] = int(correctness_indicator)
        f.close()
        incorr_count = 0
        corr_count = 0
        for j in truth_dict:
            if truth_dict[j] != self.H[j]:
                print('Incorrect:', j, truth_dict[j], self.H[j])
                incorr_count += 1
            else:
                corr_count +=1
        print('\n#Correct: {}, #Incorrect: {}\n'.format(corr_count, incorr_count))

    def dumpOptimalDecision(self, filename):
        f = open(filename, 'w')
        for j in self.H:
            f.write(str(j) + ',' + str(self.H[j]) + '\n')
        f.close()

    def dumpMeasuredVarProb(self, filename):
        f = open(filename, 'w')
        for tup in sorted(self.Z.items(), key=operator.itemgetter(1), reverse=True):
            f.write(str(tup[0]) + ',' + str(tup[1]) + '\n')
        f.close()