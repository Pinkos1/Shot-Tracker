'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: Backend for all video

'''

import cv2


class VideoManager:
    def __init__(self):
        self.cap = None
        self.video_path = None
        self.is_playing = False
        self.is_paused = False
        self.current_frame = None
        self.fps = 30


    def load_video(self, file_path):
        self.release()

        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            return False

        self.video_path = file_path

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps and fps > 0:
            self.fps = fps
        else:
            self.fps = 30

        self.is_playing = False
        self.is_paused = False
        self.current_frame = None
        return True
    

    def read_frame(self):
        if self.cap is None:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        self.current_frame = frame
        return frame

    def play(self):
        if self.cap is not None:
            self.is_playing = True
            self.is_paused = False

    def pause(self):
        if self.cap is not None:
            self.is_paused = True
            self.is_playing = False

    def stop(self):
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.is_playing = False
        self.is_paused = False
        self.current_frame = None

    def restart(self):
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.is_playing = True
        self.is_paused = False
        self.current_frame = None

    def get_delay(self):
        return max(1, int(1000 / self.fps))

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.is_playing = False
        self.is_paused = False
        self.current_frame = None
