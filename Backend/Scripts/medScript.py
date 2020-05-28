def messageHandling(messageType="error", messageContent=""):
    if(messageType == "errorFile"):
        print("ERROR! The {} could not be found.".format(messageContent))
        configFile.close()
        exit()
    elif(messageType == "warning"):
        print("WARNING! {}".format(messageContent))
    elif(messageType == "error"):
        print("ERROR!")
    
import requests
import json

# API that contains 'medicamentos' objects
apiMedUrl = "https://raw.githubusercontent.com/aspto/base-de-dados-de-medicamentos/master/listacmed.json"

configFile = open("./Config/configMedicamentos.txt", "r")
# String treatment
tableName = configFile.readline()
tableName = tableName.replace("\n", "")
outFile = configFile.readline()
outFile = outFile.replace("\n", "")
columnNames = configFile.readline()
columnNames = columnNames.replace("\n", "")

# Check if configFile is correct
if(tableName.find("tableName:") == -1):
    messageHandling("errorFile", "table name")
if(outFile.find("outFile:") == -1):
    messageHandling("errorFile", "output file")
if(columnNames.find("columnNames:") == -1):
    print(columnNames)
    messageHandling("errorFile", "column names")

tableName = tableName.replace("tableName:", '')
tableName = tableName.replace("\n", '')
outFile = outFile.replace("outFile:", '')

print("Do you want to overwrite this file ({})? (Y/N) ".format(outFile), end="")
opcao = str(input())

if(opcao.lower() == "y" or opcao.lower() == "s"):
    # Open output file
    medFile = open(outFile, "w")

    responseUrl = requests.get(apiMedUrl).text

    # Replace all ocurrences of column names on received responseUrl
    medicamentos = str(responseUrl).replace("\n        }\n        {", "},\n{")
    medicamentos = medicamentos.replace("\n            ", "")
    medicamentos = medicamentos.replace("        ", "")
    medicamentos = medicamentos.replace('"PRINCIPIO ATIVO": ', "")
    medicamentos = medicamentos.replace('"CNPJ": ', "")
    medicamentos = medicamentos.replace('"LABORATORIO": ', "")
    medicamentos = medicamentos.replace('"REGISTRO": ', "")
    medicamentos = medicamentos.replace('"EAN": ', "")
    medicamentos = medicamentos.replace('"PRODUTO": ', "")
    medicamentos = medicamentos.replace('"APRESENTACAO": ', "")
    medicamentos = medicamentos.replace('"CLASSE TERAPEUTICA": ', "")
    medicamentos = medicamentos.replace('"PMC 0%": ', "")
    medicamentos = medicamentos.replace('"PMC 12%": ', "")
    medicamentos = medicamentos.replace('"PMC 17%": ', "")
    medicamentos = medicamentos.replace('"PMC 17% ALC": ', "")
    medicamentos = medicamentos.replace('"PMC 17,5%": ', "")
    medicamentos = medicamentos.replace('"PMC 17,5% ALC": ', "")
    medicamentos = medicamentos.replace('"PMC 18%": ', "")
    medicamentos = medicamentos.replace('"PMC 18% ALC": ', "")
    medicamentos = medicamentos.replace('"PMC 20%": ', "")
    medicamentos = medicamentos.replace('"', "'")
    medicamentos = medicamentos.split('},\n{')

    medicamentos[0] = medicamentos[0].replace("\n{", "")
    medicamentos[len(medicamentos)-1] = medicamentos[len(medicamentos)-1].replace("\n}", "")

    # Converting the 'medicamentos' string to SQL statement
    templateString = "INSERT INTO " + tableName + ' VALUES ('
    for i in range(len(medicamentos)):
        medicamentos[i] = templateString + medicamentos[i] + ");"
        medFile.write(medicamentos[i]+"\n")
    # Closing file
    medFile.close()
else:
    print("No change was made in '{}'".format(outFile))