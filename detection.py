import cv2

file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
fm = 'frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(fm, file)
label = []
filename = 'labels.txt'
with open (filename, 'rt') as fpt:
#r is open and t is txt
 label = fpt.read().rstrip('\n').rsplit('\n')
 print(label)
 print(len(label))

model.setInputSize(320, 320)   
#This sets the input size of the model to 320 pixels by 320 pixel 
##The input image will be resized or cropped to this size before being fed into the model for processing.
model.setInputScale(1.0 / 127.5)
# 320.2 = 127.5 to ensure that the input data falls within a suitable range for the model's activation functions.
model.setInputMean(127.5)
#we use this to center the data around zero and remove any bias caused by lighting conditions or image capture settings.
model.setInputSwapRB(True)
#the Red and Blue channels of the input image will be swapped.
#we do this to account for differences in channel ordering conventions between different image sources or libraries.

cap = cv2.VideoCapture (0)

font_scale = 3 
font = cv2. FONT_HERSHEY_PLAIN

while True:

 ret, frame = cap.read()

 i , c, b = model.detect (frame, confThreshold=0.55)

 print (i)
 if (len (i) !=0):
      for CI, conf, boxes in zip(i. flatten (), c.flatten(), b):
         if (CI<=80):
          cv2.rectangle(frame, boxes, (150, 0, 170),2 )
          cv2.putText (frame, label[CI-1], (boxes [0]+10, boxes [1]+40), font, fontScale=font_scale, color=(255,0 ,0), thickness=1)
