
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
        results = self.model.track(frame, persist=True, verbose=False)

        people = []

        for result in results:
            boxes = result.boxes

            if boxes is None or len(boxes) == 0:
                continue

            ids = boxes.id
            if ids is None:
                continue

            for i in range(len(boxes)):
                cls_id = int(boxes.cls[i].item())
                conf = float(boxes.conf[i].item())

                if cls_id == 0 and conf >= 0.35:
                    x1, y1, x2, y2 = boxes.xyxy[i].tolist()
                    track_id = int(ids[i].item())

                    people.append({
                        "id": track_id,
                        "box": (int(x1), int(y1), int(x2), int(y2)),
                        "conf": conf
                    })

        return people
