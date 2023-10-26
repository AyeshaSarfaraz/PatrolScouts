from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model('tcp://umbertopi.local:1430', show=True, classes=0)

while True:
    for result in results:
        boxes = result.boxes
        probs = result.probs