import datetime
import threading
import socket
import json
import os
import sys
import csv
import signal
import random

# import traceback


def handler(sig, frame):  # define the handler
    print(" Bye bye!!")
    exit(0)


signal.signal(signal.SIGINT, handler)

data = {}

# abro el archivo de config y leo la direccion del archivo de cotizaciones
try:
    with open('config.txt', 'r') as configFile:
        csvFilePath = str.rstrip(configFile.readline())
except Exception as e:
    print("error")
    print(e)
    exit(1)


# preparo la tupla con la dirección del server y el buffer
serverAddressPort = ("localhost", 10000)
bufferSize = 1024

# Creo un socket cliente UDP
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# envio de la cotización


def envCotizacion():
    # abro y leo el csv
    try:
        with open(csvFilePath) as csvFile:
            csvReader = csv.DictReader(csvFile)
            for rows in csvReader:
                id = rows['id']
                data[id] = rows

        # creo JSON data y escribo en el
        jsonData = json.dumps(data, indent=4)

        # preparo los bytes a enviar
        bytesToSend = str.encode(jsonData)

        # envio al servidor de Pizarra
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        # recibo el ok de la pizarra
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        msg = "Mensaje de la Pizarra {}".format(msgFromServer[0])

        print(msg)

    except Exception as e:
        print("error")
        print(e)
        exit(1)

    # pongo fecha y hora
    currentDT = datetime.datetime.now()
    print(str(currentDT) + '\n')

    # reescribo el archivo para que haya variedad de valores
    try:
        with open(csvFilePath, 'w') as csvFile:
            csvFile.write('id,name,value1,value2\n')
            csvFile.write('1,Dolar ,' + str(random.randint(100, 12000)/100) +
                          ',' + str(random.randint(100, 12000)/100) + '\n')
            csvFile.write('2,Real  ,' + str(random.randint(100, 12000)/100) +
                          ',' + str(random.randint(100, 12000)/100) + '\n')
            csvFile.write('3,Yen   ,' + str(random.randint(100, 12000)/100) +
                          ',' + str(random.randint(100, 12000)/100) + '\n')
            csvFile.write('4,Yuan  ,' + str(random.randint(100, 12000)/100) +
                          ',' + str(random.randint(100, 12000)/100) + '\n')
            csvFile.write('5,Peseta,' + str(random.randint(100, 12000)/100) +
                          ',' + str(random.randint(100, 12000)/100) + '\n')
            csvFile.write('6,Dracma,' + str(random.randint(100, 12000)/100) +
                          ',' + str(random.randint(100, 12000)/100) + '\n')
    except Exception as e:
        print("error")
        print(e)
        exit(1)


envCotizacion()

# esperar 30 segundos es mucho, lo dejo en 10
WAIT_TIME_SECONDS = 10
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    envCotizacion()
