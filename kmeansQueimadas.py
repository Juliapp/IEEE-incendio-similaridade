import json
import pandas as pd

with open('result.json') as datafile:
    #esse json contém os caminhos pra cada dataset, podendo achar o foco
    #e o aqm com a chave ano e mês
    paths = json.load(datafile)

biomas = ["Amazonia", "Caatinga", "Cerrado", "MataAtlantica", "Pampa", "Pantanal"] 

def main(): 
    for ano in range (2016, 2019):
        for mes in range(1, 13):
            for bioma in biomas:
                    
                try:
                    strmes = mesToStr(mes)
                    #dataset totalmente filtrado, por ano mes bioma e tipo
                    aqm = getFilteredDataset(ano, strmes, bioma, 'aqm')
                    foco = getFilteredDataset(ano, strmes, bioma, 'foco')
                    '''
                    Fazer matriz de dados pra ver qual o foco mais próximo aqui
                    '''
                except:
                    continue;
               
                
def mesToStr(mes):
    if mes < 10:
        return '0' + str(mes)
    else: 
        return str(mes)


#main()
def getFilteredDataset(ano, mes, bioma, tipo):
    df = pd.read_csv(paths[ano][mes][tipo])
    return df[(df.bioma == bioma)]
