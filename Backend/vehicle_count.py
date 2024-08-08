# Import necessary packages
import cv2
import numpy as np
from Backend.tracker import *
# from tracker import *
import time
import random

""" -- Main Function to get Vehicle Count -- """
def VehicleCount(ip_addresses):
    slot_list = []
    # for camera in ip_addresses:
    for c in ip_addresses:
        # obj = YoloV3Model(c)
        # slot_list.append(obj.realTime())
        slot_list.append(random.randint(0,c))
    return slot_list


class YoloV3Model:
    def __init__(self, ip_address):
        # use ip_address of ip camera to detect vehicles from camera or give video path in vid
        # self.ip_address = "https://cdn-004.whatsupcams.com/hls/hr_pula01.m3u8"
        # self.ip_address = "http://192.168.29.61:8080/video"
        # self.vid = "parking_lot_2.mp4"
        self.ip_address = ip_address
    
        # initializing starting time and frame counter to get fps
        self.starting_time = time.time()
        self.frame_counter = 0

        # Initialize Tracker
        self.tracker = EuclideanDistTracker()

        # Initialize the videocapture object
        self.cap = cv2.VideoCapture(self.ip_address)
        self.input_size = 320

        # Detection confidence threshold
        self.confThreshold =0.4
        self.nmsThreshold= 0.4

        self.font_color = (0, 0, 255)
        self.font_size = 0.5
        self.font_thickness = 2

        self.classNames = ['person','bicycle','car','motorbike','aeroplane','bus','train','truck','boat','traffic light','fire hydrant',
        'stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella',
        'handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard',
        'tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog',
        'pizza','donut','cake','chair','sofa','pottedplant','bed','diningtable','toilet','tvmonitor','laptop','mouse','remote','keyboard',
        'cell phone','microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear','hair drier','toothbrush']

        # class index for our required detection classes
        self.required_class_index = [2, 3, 5, 7]
        self.detected_classNames = []

        ## Model Files
        modelConfiguration = r'Backend\yolov3-320.cfg'
        modelWeigheights = r'Backend\yolov3-320.weights'
        # configure the network model
        self.net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)

        # Configure the network backend if CUDA is installed
        # self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        # Define random colour for each class
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.classNames), 3), dtype='uint8')


    # Function for finding the detected objects from the network output
    def postProcess(self, outputs, vc): 
        height, width = self.img.shape[:2]
        boxes = []
        classIds = []
        confidence_scores = []
        detection = []
        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if classId in self.required_class_index:
                    if confidence > self.confThreshold:
                        # print(classId)
                        w,h = int(det[2]*width) , int(det[3]*height)
                        x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                        boxes.append([x,y,w,h])
                        classIds.append(classId)
                        confidence_scores.append(float(confidence))
        # Apply Non-Max Suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, self.confThreshold, self.nmsThreshold)
        # print(classIds)

        # if we did not found any indices
        if len(indices) == 0:
            return
        # print(type(indices), len(indices))

        for i in indices.flatten():
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            # print(x,y,w,h)

            color = [int(c) for c in self.colors[classIds[i]]]
            name = self.classNames[classIds[i]]
            self.detected_classNames.append(name)
            
            # Draw classname and confidence score 
            cv2.putText(self.img, f'{name.upper()} {int(confidence_scores[i]*100)}%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw bounding rectangle
            cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 1)
            
            detection.append([x, y, w, h, self.required_class_index.index(classIds[i])])

        # Up date the tracker for each object
        boxes_ids = self.tracker.update(detection)

        # printing number of vehicles
        print('Vehicles :', str(len(boxes_ids)), end="  ")
        vc.append(len(boxes_ids))


    def realTime(self):
        vc = []
        for i in range(3):
            success, self.img = self.cap.read()
            if success == False:
                break
            
            self.frame_counter += 1
            self.img = cv2.resize(self.img,(0,0),None,0.5,0.5)
            # ih, iw, channels = self.img.shape
            blob = cv2.dnn.blobFromImage(self.img, 1 / 255, (self.input_size, self.input_size), [0, 0, 0], 1, crop=False)

            # Set the input of the network
            self.net.setInput(blob)
            layersNames = self.net.getLayerNames()

            # '''------@_@CHANGE i[0] -> i -------'''
            outputNames = [(layersNames[i[0] - 1]) for i in self.net.getUnconnectedOutLayers()]
            # Feed data to the network
            outputs = self.net.forward(outputNames)
    
            # Find the objects from the network output
            self.postProcess(outputs, vc)

            endingTime = time.time() - self.starting_time
            fps = self.frame_counter/endingTime
            print("fps :", str(fps))

            # Show the frames
            # cv2.imshow('Output', self.img)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
    
        print(vc)
        if len(vc) == 0:
            return 0
        return np.bincount(vc).argmax()
    

'''------------------Driver Code---------------------'''

vid = ['Backend/parking_lot_1.mp4', 'Backend/parking_lot_2.mp4', 'Backend/parking_lot_3.avi', 'Backend/parking_lot_4.mp4']
# print((cv2.VideoCapture(vid[0]).read()[0]))
# print(VehicleCount(vid))

'''-----------------------------------------------------------'''
