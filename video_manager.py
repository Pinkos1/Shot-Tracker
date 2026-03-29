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
    