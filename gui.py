
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




    def open_video(self):
        file_path = filedialog.askopenfilename(
            title = "Select a Video File",
            filetypes = [
                ("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        success = self.video_manager.load_video(file_path)

        if not success:
            messagebox.showerror("Error", "Could not open the video.")
            return

        self.label.config(text = os.path.basename(file_path))

        first_frame = self.video_manager.read_frame()
        if first_frame is not None:
            processed_frame = self.process_frame(first_frame)
            self.show_frame(processed_frame)

        self.video_manager.pause()



    def play_video(self):
        if self.video_manager.cap is None:
            messagebox.showwarning("No Video", "Please choose a video first.")
            return

        self.video_manager.play()


    def pause_video(self):
        self.video_manager.pause()


    def stop_video(self):
        self.video_manager.stop()
        self.clear_video_display()


    def restart_video(self):
        if self.video_manager.cap is None:
            messagebox.showwarning("No Video", "Please choose a video first.")
            return

        self.video_manager.restart()


    def toggle_people_detection(self):
        if self.is_processing_frame:
            return

        self.detect_people_enabled = not self.detect_people_enabled

        if self.detect_people_enabled:
            self.people_button.config(text = "Players: ON")
        else:
            self.people_button.config(text = "Players: OFF")


    def toggle_rim_detection(self):
        if self.is_processing_frame:
            return

        self.detect_rims_enabled = not self.detect_rims_enabled

        if self.detect_rims_enabled:
            self.rim_button.config(text = "Rim: ON")
        else:
            self.rim_button.config(text = "Rim: OFF")


    def process_frame(self, frame):
        raw_frame = frame.copy()
        processed = frame.copy()

        people_count = 0
        rim_count = 0


        if self.detect_rims_enabled:
            try:
                rims = self.rim_detector.detect_rims(raw_frame)
                rim_count = len(rims)
                processed = self.rim_detector.draw_rims(processed, rims)
                print("Rims found:", rim_count)
            except Exception as e:
                print("Rim detection error:", e)
                cv2.putText(
                    processed,
                    "Rim Detection Error",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )
        if self.detect_people_enabled:
            try:
                people = self.person_detector.detect_and_track(raw_frame)
                people_count = len(people)
                processed = self.person_detector.draw_people(processed, people)
            except Exception as e:
                print("Player detection error:", e)
                cv2.putText(
                    processed,
                    "Player Detection Error",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

        cv2.putText(
            processed,
            f"Players: {people_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2
        )

        cv2.putText(
            processed,
            f"Rims: {rim_count}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 165, 255),
            2
        )

        return processed
    



    