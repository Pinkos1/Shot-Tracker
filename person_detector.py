
'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: File detects players on the floor

'''
from ultralytics import YOLO
import cv2

class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
    

    def detect_and_track(self, frame):
        results = self.model.track(frame, persist = True, verbose = False)
