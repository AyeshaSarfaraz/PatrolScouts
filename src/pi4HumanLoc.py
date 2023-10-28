from socket import *
from pymavlink import mavutil
from time import sleep

PI4NAME = 'umbertopi.local'
PI4PORT = 1530
BAUDRATE = 57600


def createPixConnection():
    the_connection = mavutil.mavlink_connection('/dev/serial0', BAUDRATE)
    the_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
    return the_connection


def getLocationPix(pixConnection):
    coordinate = []

    while True:
        try:
            
            longitude =  pixConnection.messages['GPS_RAW_INT'].lon
            latitude =  pixConnection.messages['GPS_RAW_INT'].lat
            #timestamp = pixConnection.time_since('GPS_RAW_INT')
            coordinate.append(latitude)
            coordinate.append(longitude)
            print(f"Coordinates: {coordinate}")
            break
        except:
            print('No GPS_RAW_INT message received')
            sleep(1)
    
    if coordinate:
        latStr = str(coordinate[0])
        latStr = latStr[:2] + '.' + latStr[2:]
        lonStr = str(coordinate[1])
        lonStr = lonStr[:2] + '.' + lonStr[2:]
        return f"Coordinates: {latStr}, {lonStr}"



piSocket = socket(AF_INET, SOCK_STREAM)
piSocket.bind((PI4NAME, PI4PORT))
piSocket.listen(1)

print('The PI4 is ready to receive requests')

try:
    pixConnection = createPixConnection()
except:
    print('Could not establish connection with PixHawk')
    quit()

while True:
    connectionSocket, ConnectionAddr = piSocket.accept()

    request = connectionSocket.recv(1024)
    request = request.decode()

    if (request == 'GET LOCATION'):
        locObtained = getLocationPix(pixConnection)
        connectionSocket.send(locObtained.encode())
    
    connectionSocket.close()


