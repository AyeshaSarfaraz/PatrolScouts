from ultralytics import YOLO

from socket import *


ACCEPTEDCONF = 0.5

PI4NAME = 'umbertopi.local'
PI4PORT = 1530

def requestLoc():
    gcsSocket = socket(AF_INET, SOCK_STREAM)
    gcsSocket.connect((PI4NAME, PI4PORT))

    request = 'GET LOCATION'

    gcsSocket.send(request.encode())

    locObtainedFromPi = gcsSocket.recv(1024)
    locObtainedFromPi = locObtainedFromPi.decode()
    print('**************************************************************************')
    print('**************************************************************************')
    print('**************************************************************************')
    print(locObtainedFromPi)
    print('**************************************************************************')
    print('**************************************************************************')
    print('**************************************************************************')

    gcsSocket.close()

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
                        requestLoc()


humanDetect()