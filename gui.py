
'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: gui for the program, allows to select video, pause, play and choose what is being detected. 
'''


import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from video_manager import VideoManager
from person_detector import PersonDetector
from rim_detector import RimDetector

class VideoPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Basketball Shot Tracker - Video Player")
        self.root.geometry("1100x750")



        self.video_manager = VideoManager()
        self.person_detector = PersonDetector()
        self.rim_detector = RimDetector()

        self.photo = None
        self.detect_people_enabled = True
        self.detect_rims_enabled = True
        self.is_processing_frame = False

        self.create_widgets()
        self.update_loop()


    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.open_button = tk.Button(
            top_frame,
            text="Open Video",
            command=self.open_video,
            width=12
        )

    