
'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: File detects players on the floor

'''


class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
