
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
        self.root.title("Basketball Shot Tracker")
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
        top_frame.pack(side = tk.TOP, fill = tk.X, padx = 10, pady = 10)

        self.open_button = tk.Button(
            top_frame,
            text = "Open Video",
            command = self.open_video,
            width = 12
        )

        self.open_button.pack(side = tk.LEFT, padx = 5)



        self.play_button = tk.Button(
            top_frame,
            text = "Play",
            command = self.play_video,
            width = 10
        )
        self.play_button.pack(side = tk.LEFT, padx = 5)



        self.pause_button = tk.Button(
            top_frame,
            text = "Pause",
            command = self.pause_video,
            width = 10
        )
        self.pause_button.pack(side = tk.LEFT, padx = 5)



        self.stop_button = tk.Button(
            top_frame,
            text = "Stop",
            command = self.stop_video,
            width = 10
        )
        self.stop_button.pack(side = tk.LEFT, padx = 5)



        self.restart_button = tk.Button(
            top_frame,
            text = "Restart",
            command = self.restart_video,
            width = 10
        )
        self.restart_button.pack(side = tk.LEFT, padx = 5)



        self.people_button = tk.Button(
            top_frame,
            text = "Players: ON",
            command = self.toggle_people_detection,
            width = 12
        )
        self.people_button.pack(side = tk.LEFT, padx = 5)



        self.rim_button = tk.Button(
            top_frame,
            text = "Rim: ON",
            command = self.toggle_rim_detection,
            width = 10
        )
        self.rim_button.pack(side = tk.LEFT, padx = 5)



        self.label = tk.Label(
            top_frame,
            text = "No video selected",
            anchor = "w"
        )
        self.label.pack(side = tk.LEFT, padx = 10)



        self.video_label = tk.Label(self.root, bg = "black")
        self.video_label.pack(fill=tk.BOTH, expand = True, padx = 10, pady = 10)


    