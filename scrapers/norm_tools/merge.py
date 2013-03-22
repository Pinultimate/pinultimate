import os
import sys
import json
import math
import random
from normalize import *



class Merge:
	def __init__(self):
		random.seed()
		self.dataSets = []
		self.weight = []
		self.data = []
		self.FACTOR = 10

	def addData(self, json_data, json_weight):
		self.dataSets.append(json_data)
		self.weight.append(float(json_weight))

	def normalizeWeight(self):
		miu = sum(self.weight) / len(self.weight)
		for w in self.weight:
			w -= miu
		sigmaSquare = 0
		for w in self.weight:
			sigmaSquare += math.pow(w, 2)
			sigma = math.sqrt(sigmaSquare / len(self.weight))
			for w in self.weight:
				w =  int ((w / sigma) * self.FACTOR)
				if w < 0:
					w = 0

	def densityBasedMerge(self):
		self.normalizeWeight()
		for idx, dataEntry in enumerate(self.dataSets):
			norm = Normalize(dataEntry)
			if 'value' in dataEntry[0]:
				norm.normValue()
				norm.valueToDensity(self.weight[idx])
			else:
				norm.adjustDensity(self.weight[idx])
			for checkIn in norm.data:
					self.data.append(checkIn)
		newData = Normalize(self.data)
		newData.normDensity()
		#newData.densityToValue() Generates value points
		self.data = newData.data

	def valueBasedMerege(self):
		self.normalizeWeight()
		for idx, dataEntry in enumerate(self.dataSets):
			if 'value' in dataEntry[0]:
				for checkIn in dataEntry:
					checkIn['value'] = float(checkIn['value']) * self.weight[idx]
					self.data.append(checkIn)
			else:
				for checkIn in dataEntry:
					checkIn['value'] = self.weight[idx]
					self.data.append(checkIn)
		newData = Normalize(self.data)
		newData.normValue()
		newData.valueToDensity(self.FACTOR)  #Generates density points
		self.data = newData.data


