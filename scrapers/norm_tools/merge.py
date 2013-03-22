import os
import sys
import json
import math
import random
import normalize



class Merge:
	def __init__(self):
        random.seed()
        self.dataSets = []
        self.weight = []
        self.data = []
        self.FACTOR = 10


    def addData(self, json_data, json_weight):
    	self.dataSets.append(json_data)
    	self.weight.append(float(json_weight)

    def normalizeWeight(self):
    	miu = sum(self.weight) / len(self.weight)
    	for w in self.weight
    		w -= miu
    	sigmaSquare = 0
    	for w in self.weight
    		sigmaSquare += math.pow(w, 2)
    	sigma = math.fsqrt(sigmaSaquare / len(self.weight))
    	for w in self.weight
    		w =  int ((w / sigma) * self.FACTOR)

    def densityBasedMerge(self):
    	for idx, dataEntry in dataSets:
    		norm = Normalize(dataEntry)
    		if 'value' in dataEntry:
    			norm.normValue()
    			norm.valueTodensity(self.weight[idx])
    		else:
    			nomr.adjustDensity(self.weight[idx])
    		for checkIn in norm.data:
    				self.data.append(checkIn)
    	newData = Normalize(self.data)
    	newData.normDensity()
    	#newData.densityToValue() Generates value points
    	return newData.data

    def valueBasedMerege(self):
    	for idx, dataEntry in dataSets:
    		if 'value' in dataEntry:
    			for checkIn in dataEntry:
    				checkIn['value'] *= self.weight[idx]
    				self.data.append(checkIn)
    		else:
    			for checkIn in dataEntry:
    				checkIn['value'] = self.weight[idx]
    				self.data.append(checkIn)
    	newData = Normalize(self.data)
    	newData.normValue()
    	newData.valueToDensity(self.FACTOR)  #Generates density points
    	return newData.data


