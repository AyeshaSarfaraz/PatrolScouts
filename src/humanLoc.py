from ultralytics import YOLO
from pymavlink import mavutil
from socket import *

ACCEPTEDCONF = 0.5


def requestLoc():
    PI4NAME = 'umbertopi.local'
    PI4PORT = 1530

    gcsSocket = socket(AF_INET, SOCK_STREAM)
    gcsSocket.connect((PI4NAME, PI4PORT))

    request = 'GET LOCATION'

    gcsSocket.send(request.encode())

    coordinates = gcsSocket.recv(1024)

    coordinates = coordinates.decode()

    gcsSocket.close()

    return coordinates

def humanDetect():
    model = YOLO('yolov8n.pt')
    results = model('tcp://umbertopi.local:1430', show=True, classes=0, stream=True)
    #results = model(0,show=True, classes=0, stream=True)
    while True:
        for result in results:
            boxes = result.boxes
            probs = result.probs
            print(boxes.conf.tolist())

            if len(boxes.conf.tolist()) > 0:
                for detectionConf in boxes.conf.tolist():
                    if detectionConf >= ACCEPTEDCONF:
                        getLocation()
        


humanDetect()