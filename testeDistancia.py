# -*- coding: utf-8 -*-
"""
[[  4.36  -60.785]]
[[  4.36  -60.785]
 [  4.36  -60.785]
 [  4.36  -60.785]
 ...
 [  4.36  -60.785]
 [  4.36  -60.785]
 [  4.36  -60.785]]
"""
import numpy as np
from math import sin, cos, sqrt, atan2, radians

R = 6373.0

a = np.array([  4.36,  -60.785])

b = np.array([[  4.36,  -60.785],
 [  4.36,  -60.785],
 [  4.36,  -61.785],
 [  4.36,  -60.785],
 [  4.36,  -60.785],
 [  4.36,  -60.785]])


#retorna o índice do menor valor 
def calculateIndexMinorDistance(pointAqm, focos):
    lat1 = radians(pointAqm[0])
    lon1 = radians(pointAqm[1])

    #resultados das comparações
    result = np.empty(shape=[0, 1], dtype=float)
    for foco in focos:
           lat2 = radians(foco[0])
           lon2 = radians(foco[1])
           
           dlon = lon2 - lon1
           dlat = lat2 - lat1
           a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
           c = 2 * atan2(sqrt(a), sqrt(1 - a))
           distance = R * c
           result = np.append(result, np.array([[distance]]), axis=0)
           
    #resgatando o índice do menor valor 
    minValueIndex = 0
    minValue = 0
    
    print(result)
    for i, r in enumerate(result):
        if((r < minValue and r != 0) or (minValue == 0 and r != 0)):
            minValue = r
            minValueIndex = i

    
    return minValueIndex


calculateDistances(a, b)
