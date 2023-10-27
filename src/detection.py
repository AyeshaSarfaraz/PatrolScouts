from ultralytics import YOLO

ACCEPTEDCONF = 0.5

model = YOLO('yolov8n.pt')
#results = model('tcp://umbertopi.local:1430', show=True, classes=0)
results = model(0,show=True, classes=0, stream=True)
while True:
    for result in results:
        boxes = result.boxes
        probs = result.probs
        print(boxes.conf.tolist())
        
        if len(boxes.conf.tolist()) > 0:
            for detectionConf in boxes.conf.tolist():
                if detectionConf >= ACCEPTEDCONF:
                    pass
        