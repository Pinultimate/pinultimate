import os
import sys
import json
import math
import random

class Normalize:        

    def __init__(self, json_data):
        self.data = json_data
        self.Threshhold = 0
        random.seed()

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



    # Find the clusters 
    def cluster(self):
        CLUSTER_GAP = 0.001
        MIN_GAP = 0.001
        CLUSTER_RATIO = 0.5
        self.getCord()
        num = len(self.data)
        maxLat = max(self.lat)
        minLat = min(self.lat)
        maxLng = max(self.lng)
        minLng = min(self.lng)
       
        cluster_num = int(num * CLUSTER_RATIO)
        #cluster_num = int((math.fabs((maxLat - minLat)) + CLUSTER_GAP) * (math.fabs(maxLng - minLng) + CLUSTER_GAP) / CLUSTER_GAP)
        miu = []

        for i in xrange(cluster_num):
            miu.append(self.data[random.randint(0, num - 1)])

        c = [0]*num

        return_flag = 0
        while return_flag == 0:
            return_flag = 1
            count = [0]*cluster_num
            latSum = [0]*cluster_num
            lngSum = [0]*cluster_num
            for i in xrange(num):
                minDistance = 6480
                minIndex = c[i]
                for j in xrange(cluster_num):
                    distance = pow(self.data[i]['latitude'] - miu[j]['latitude'], 2) + pow(self.data[i]['longitude'] - miu[j]['longitude'], 2) 
                    if distance < minDistance:
                        minDistance = distance
                        minIndex = j
                c[i] = minIndex
                count[minIndex] += 1
                #valueSum[minIndex]
                latSum[minIndex] += float(self.data[i]['latitude'])
                lngSum[minIndex] += float(self.data[i]['longitude'])
            return_flag = 1
            for k in xrange(cluster_num):
                newLat = latSum[k] / count[k]
                newLng = lngSum[k] / count[k]
                if math.fabs(miu[k]['latitude'] - newLat) > MIN_GAP:
                    miu[k]['latitude'] = newLat
                    return_flag = 0
                if math.fabs(miu[k]['longitude'] - newLng) > MIN_GAP: 
                    miu[k]['longitude'] = newLng
                    return_flag = 0
        return (num, cluster_num, count, miu, c)

    #Find clusters and only keep points within certain radius of the cluster 
    def normDensity(self):
        num, cluster_num, count, miu, c = self.cluster()
        newData = []
        RANGE = 1
        for m in xrange(num):
            distance = pow(self.data[m]['latitude'] - miu[c[m]]['latitude'], 2) + pow(self.data[m]['longitude'] - miu[c[m]]['longitude'], 2) 
            if distance < RANGE:
                newCheckIn = self.data[m]
                newData.append(newCheckIn)
        self.data = newData



    #Use k-means clustering to change density based data to less points with value
    def densityToValue(self):
        num, cluster_num, count, miu, c = self.cluster()


        newData = []
        for m in xrange(cluster_num):
            newCheckIn = {'latitude': miu[m]['latitude'], 'longitude': miu[m]['longitude'], 'value': count[m]}
            newData.append(newCheckIn)
        self.data = newData


    #Assume normal distribution  
    def valueToDensity(self):
        GAP = 0.001
        FACTOR = 1 # Unit normalized value will generate FACTOR number of points
        self.getCord()
        self.getValue()
        num = len(self.data)
        maxLat = max(self.lat)
        minLat = min(self.lat)
        maxLng = max(self.lng)
        minLng = min(self.lng)

        sigma = math.sqrt((math.fabs((maxLat - minLat)) + GAP) * (math.fabs(maxLng - minLng) + GAP) / num)  
        newData = []
        for checkIn in self.data:
            for i in xrange(int(checkIn['value']) * FACTOR):
                newCheckIn = {'latitude': random.gauss(checkIn['latitude'], sigma), 'longitude': random.gauss(checkIn['longitude'], sigma)}
                newData.append(newCheckIn)
        self.data = newData






        
        
