

'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: File detects players on the floor

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
            source=frame,
            conf=0.05,
            iou=0.30,
            verbose=False
        )

        best_rim = None
        best_conf = 0.0

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                conf = float(box.conf[0].item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                if conf > best_conf:
                    best_conf = conf
                    best_rim = {
                        "box": (int(x1), int(y1), int(x2), int(y2)),
                        "conf": conf
                    }

        if best_rim is not None:
            return [best_rim]

        return []

    def draw_rims(self, frame, rims):
        for rim in rims:
            x1, y1, x2, y2 = rim["box"]
            conf = rim["conf"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 3)

            cv2.putText(
                frame,
                f"Rim {conf:.2f}",
                (x1, max(25, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 165, 255),
                2
            )

        return frame