import requests
import json
import unicodedata

apiDoencaUrl = "https://cid10-api.herokuapp.com/cid10"
outFile = "doencas.txt"

print("Do you want to overwrite this file ({})? (S/N) ".format(outFile), end="")
opcao = str(input())

# oppening config file
configFile = open("config.txt", "r")
nomeTabela = configFile.readline()
outFile = configFile.readline()

# check if config file is correct
if(nomeTabela.find("tableName") == -1):
    print("ERROR! The table name could not be found.")
    exit()
if(outFile.find("outFile") == -1):
    print("ERROR! The output file could not be found.")
    exit()

nomeTabela = nomeTabela.replace("tableName:", '')
nomeTabela = nomeTabela.replace("\n", '')
outFile = outFile.replace("outFile:", '')

if(opcao.lower() == "s"):
    print("The file will be overwrited!")
    doencasFile = open(outFile, "w") # Opening file in write mode

    respostaUrl = requests.get(apiDoencaUrl) # Get values from URL
    jsonParsed = json.loads(respostaUrl.text) # Convert values in unicode to utf8

    doencas = str(jsonParsed).split('}, {') # Separating objects

    tamListDoencas = len(doencas)
    
    doencas[0] = doencas[0].replace('[{', '')
    doencas[tamListDoencas-1] = doencas[tamListDoencas-1].replace('}]', '')

    for i in range(tamListDoencas):
        stringDoenca = "INSERT INTO " + nomeTabela + " VALUES ("
        doencas[i] = doencas[i].replace("'codigo': ", '')
        doencas[i] = doencas[i].replace("'nome': ", '')
        stringDoenca += doencas[i]
        stringDoenca += ");"
        doencas[i] = stringDoenca
        doencasFile.write(doencas[i] + "\n")
    
    doencasFile.close() # Closing file
    print("Process Done! Thank you!")
else:
    print("No change was made in '{}'".format(outFile))