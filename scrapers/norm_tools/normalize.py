import os
import sys
import json
import math

class Normalize:        

    

    def __init__(self, json_data):
        self.data = json_data
        self.Threshhold = 0

    def getValue(self):
        self.value = []
        for checkIn in self.data:
            self.value.append(int(checkIn['value']))

    def getCord(self):
        self.lat = []
        self.lng = []
        for checkIn in self.data:
            self.lat.append(float(checkIn['latitude']))
            self.lng.append(float(checkIn['longitude']))


    #Take the value based checkins and normalize it 
    def normValue(self):
        self.getValue()
        miu = float(sum(self.value)) / len(self.value)
        sigmaSquare = 0
        for idx, val in enumerate(self.value):
            self.value[idx] -= miu
            sigmaSquare += math.pow(self.value[idx], 2)
        sigma = math.sqrt(sigmaSquare / len(self.value))
        newData = []
        for idx, val in enumerate(self.data):
            newValue = self.value[idx] / sigma
            if newValue > self.Threshhold:
                newCheckIn = {'latitude': self.data[idx]['latitude'], 'longitude': self.data[idx]['longitude'], 'value': newValue}
                newData.append(newCheckIn)
        self.data = newData

    #
    def normDensity(self):
        print "density"

    #Use k-means clustering
    def densityToValue(self):
        CLUSTER_GAP = 0.001
        self.getCord()
        maxLat = max(self.lat)
        minLat = min(self.lat)
        maxLng = max(self.lng)
        minLng = min(self.lng)
        cluster_num = (math.fabs((maxLat - minLat)) + CLUSTER_GAP) * (math.fabs(maxLng - minLng) + CLUSTER_GAP) / CLUSTER_GAP
        
        
        print cluster_num
        print "k-means clustering"

    #Assume normal distribution  
    def valueToDensity(self, timeRange, ):
        print "hello"
        
