import json
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians

#Raio aproximado da terra
R = 6373.0

with open('result.json') as datafile:
    #esse json contém os caminhos pra cada dataset, podendo achar o foco
    #e o aqm com a chave ano e mês
    paths = json.load(datafile)

biomas = ["Amazonia", "Caatinga", "Cerrado", "MataAtlantica", "Pampa", "Pantanal"] 

def main(): 
    num = 0
    for ano in range (2016, 2020):
        for mes in range(1, 13):
            for bioma in biomas:
                
                strmes = mesToStr(mes)
                pathAqm = getPath(str(ano), strmes, 'aqm')
                pathFoco = getPath(str(ano), strmes, 'foco')
                if(pathAqm and pathFoco):
                    df1 = pd.read_csv(pathAqm)
                    df2 = pd.read_csv(pathFoco)
                    aqm = df1[(df1.bioma == bioma)]
                    foco = df2[(df2.bioma == bioma)]  
                    num += 1
                    populateDataset(aqm, foco, str(ano), strmes, bioma, num)


def getPath(ano, mes, tipo):
    try:
        return paths[ano][mes][tipo]
    except:
        return None

  
def mesToStr(mes):
    if mes < 10:
        return '0' + str(mes)
    else: 
        return str(mes)

def populateDataset(aqm, foco, ano, mes, bioma, num):
    COLUMN_NAMES=['latitude','longitude','bioma','area(m²)','diasemchuva','precipitacao','riscofogo']
    df = pd.DataFrame(columns=COLUMN_NAMES)    
    count = 0;
    lenght = len(aqm)
    
    for index, aqmRow in aqm.iterrows():
        pointAqm = np.array([[aqmRow['latitude'], aqmRow['longitude']]])
        focos = np.empty((0, 2), dtype=float)
        
        for index2, focoRow in foco.iterrows():
            focos =  np.append(focos, np.array([[focoRow['latitude'], focoRow['longitude']]]), axis=0)

        i = calculateIndexMinorDistance(pointAqm, focos)
        realAqm = foco.iloc[i]
        
        df = df.append({'latitude' : aqmRow['latitude'] ,'longitude' : aqmRow['longitude'] ,'bioma' : aqmRow['bioma'] ,'area(m²)' : aqmRow['area(m²)'] ,'diasemchuva' : realAqm['diasemchuva'] ,'precipitacao' : realAqm['precipitacao'] , 'riscofogo' : realAqm['riscofogo']}, ignore_index=True)
        print('appending: ' + str(count) + ' from: ' + str(lenght) + ' rows | in dataset ' + str(num) + ' from: 288‬')
        count += 1
        
    outName = 'Predicted/' + bioma + '_' + ano + '_' + mes + '.csv'
    df.to_csv(outName)
    

#retorna o índice do menor valor 
def calculateIndexMinorDistance(pointAqm, focos):
    lat1 = radians(pointAqm[0][0])
    lon1 = radians(pointAqm[0][1])

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

    for i, r in enumerate(result):
        if((r < minValue and r != 0) or (minValue == 0 and r != 0)):
            minValue = r
            minValueIndex = i

    
    return minValueIndex


main()    
