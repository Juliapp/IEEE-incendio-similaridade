import pandas as pd
import json

dictData = {"Amazonia" : {}, "Caatinga" : {}, "Cerrado" : {}, "MataAtlantica" : {}, "Pampa" : {}, "Pantanal" : {}} 


def loadDict():
    dict = {}
    
    for ano in range (2016, 2020):
        dict[str(ano)] = {}
        #percorre todos os meses
        for mes in range(1, 13):
            
            aqmMeses = []
            focosMeses = []
            
            #pega todas as regiões daquele mes
            for b in dictData:
                if (mes < 10):
                    aqmFileName ='Original/' + b +'_'+str(ano)+'_0'+str(mes)+'_aqm.csv'
                    focosFileName = 'Original/' + 'Focos'+b+'_'+str(ano)+'_0'+str(mes)+'.csv'
                else:
                    aqmFileName = 'Original/' + b+'_'+str(ano)+'_'+str(mes)+'_aqm.csv'
                    focosFileName = 'Original/' + 'Focos'+b+'_'+str(ano)+'_'+str(mes)+'.csv'
                #para cada região daquele mes juntar no dataframe os dados
                try:
                    aqmFile = pd.read_csv(aqmFileName)
                    focosFile = pd.read_csv(focosFileName)
                    
                    #adicionando a coluna bioma ao dataframe
                    aqmFile['bioma'] = b
                    focosFile['bioma'] = b
                    
                    #adicionando ao csv total desse ano
                    aqmMeses.append(aqmFile)
                    focosMeses.append(focosFile)
                except:
                    continue;  
                    
            #joga todas as regiões pra um csv
            try:
                if (mes < 10):
                    strMes = '0' + str(mes)
                else:
                    strMes = str(mes)
                #nome dos arquivos
                outAqmName = 'Merged/Queimadas' + str(ano) + '_' + strMes + '.csv'
                outFocoName = 'Merged/Focos' +str(ano) + '_' + strMes + '.csv'
                
                #merge do array de datasets
                frameAqm = pd.concat(aqmMeses)
                frameFoco = pd.concat(focosMeses)
                
                frameAqm = frameAqm.drop('id', axis=1)
                
                frameAqm.index.name = 'index'
                frameFoco.index.name = 'index'
                
                frameAqm = frameAqm.reindex()
                frameFoco = frameFoco.reindex()
                
                
                #transformando em arquivo csv
                frameAqm.to_csv(outAqmName)
                frameFoco.to_csv(outFocoName)
                
                dict[str(ano)].update({strMes: {"aqm" : outAqmName, "foco" : outFocoName}})

            except:
                continue;
                
    #os arquivos no final estarão num para indicar qual o diretório de cada

    with open('result.json', 'w') as fp:
        json.dump(dict, fp)
    
    

loadDict()
