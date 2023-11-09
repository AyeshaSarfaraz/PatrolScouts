from ultralytics import YOLO
from time import sleep
from socket import *


ACCEPTEDCONF = 0.5

PI4NAME = 'milopi.local'
PI4PORT = 1530


request = 'GET LOCATION'

def createSocket():
    gcsSocket = socket(AF_INET, SOCK_STREAM)
    try:
        gcsSocket.connect((PI4NAME, PI4PORT))
    except ConnectionRefusedError as e:
        print(f"Connection to {PI4NAME}:{PI4PORT} refused: {e}")
    except Exception as e:
        print(f"An error occurred while connecting: {e}")
    return gcsSocket

def requestLoc(gcsSocket):
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

    return True

    

def humanDetect():
    model = YOLO('yolov8n.pt')
    results = model('tcp://milopi.local:1432', show=True, classes=0, stream=True)
    #results = model(0,show=True, classes=0, stream=True)
    try:
        gcsSocket = createSocket()
    except:
        print('Cannot open GCS Socket')
        return

    while True:
        for result in results:
            boxes = result.boxes
            probs = result.probs
            print(boxes.conf.tolist())

            if len(boxes.conf.tolist()) > 0:
                for detectionConf in boxes.conf.tolist():
                    if detectionConf >= ACCEPTEDCONF:
                        while not requestLoc(gcsSocket):
                            continue
                    break
            



humanDetect()
