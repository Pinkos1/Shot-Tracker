

'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: File detects basketball rims

'''

from ultralytics import YOLO
import cv2


class RimDetector:

    def __init__(self):
        self.model = YOLO("best_rim.pt")
        print("Rim model loaded.")
        print("Class names:", self.model.names)

    def detect_rims(self, frame):
        results = self.model.predict(
            source = frame,
            conf = 0.05,
            iou = 0.30,
            verbose = False
        )