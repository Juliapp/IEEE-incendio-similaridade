import json
import pandas as pd
import numpy as np
from scipy.spatial import distance

with open('result.json') as datafile:
    #esse json contém os caminhos pra cada dataset, podendo achar o foco
    #e o aqm com a chave ano e mês
    paths = json.load(datafile)

biomas = ["Amazonia", "Caatinga", "Cerrado", "MataAtlantica", "Pampa", "Pantanal"] 

def main(): 
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
                    populateNewDataset(aqm, foco)


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

def populateNewDataset(aqm, foco):
    for index, aqmRow in aqm.iterrows():
        x1 = aqmRow['latitude']
        y1 = aqmRow['longitude']
        pointAqm = np.array([[x1, y1]])
        focos = np.empty((0, 2), dtype=float)
        
        for index2, focoRow in foco.iterrows():
            x2 = focoRow['latitude']
            y2 = focoRow['longitude']
            focos = np.append(focos, np.array([[x2, y2]]), axis=0)

        distances = distance.cdist(pointAqm, focos, 'euclidean')
        result = np.amin(distances, axis=1)
        print('O resultado foi: ', result)
            

main()       