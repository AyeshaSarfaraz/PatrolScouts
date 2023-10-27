from socket import *
from pymavlink import mavutil

PI4NAME = 'umbertopi.local'
PI4PORT = 1530
BAUDRATE = 57600

def getLocationPix():
    coordinate = []
    
    try:
        longitude =  the_connection.messages['GPS_RAW_INT'].lon
        latitude =  the_connection.messages['GPS_RAW_INT'].lat
        timestamp = the_connection.time_since('GPS_RAW_INT')
        coordinate.append(latitude/100)
        coordinate.append(longitude/100)
        print(f"Coordinates: {coordinate}")
    except:
        print('No GPS_RAW_INT message received')
    
    return f"Coordinates: {coordinate[0]}, {coordinate[1]}"



the_connection = mavutil.mavlink_connection('/dev/serial0', BAUDRATE)
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))


piSocket = socket(AF_INET, SOCK_STREAM)
piSocket.bind((PI4NAME, PI4PORT))
piSocket.listen(1)

print('The PI4 is ready to receive requests')

while True:
    connectionSocket, ConnectionAddr = piSocket.accept()

    request = connectionSocket.recv(1024)
    request = request.decode()

    if (request == 'GET LOCATION'):
        locObtained = getLocationPix()
        connectionSocket.send(locObtained.encode())
    
    connectionSocket.close()


