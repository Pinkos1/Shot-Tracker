##
# @file gui.py
# @author Adam Pinkos
# @date March 22, 2026
# @brief GUI for the shot tracker program
#
# @details
# This file implements the graphical user interface (GUI) for the application.
# It allows the user to:
# - Select a video file
# - Play and pause the video
# - Control playback
# - Choose which objects are detected
#


import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from video_manager import VideoManager
from person_detector import PersonDetector
from rim_detector import RimDetector




##
# @class VideoPlayerGUI
# @brief Main GUI class for the basketball shot tracker
#
# @details
# This class creates the application window, manages user controls,
# processes video frames, and displays object detection results.
#
class VideoPlayerGUI:
    ##
    # @brief Initializes the GUI and application objects
    #
    # @param root The main Tkinter window
    #
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



    ##
    # @brief Creates all GUI widgets for the application
    #
    # @details
    # This includes buttons for opening, playing, pausing, stopping,
    # and restarting the video, along with buttons for toggling
    # player and rim detection.
    #
    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.open_button = tk.Button(
            top_frame,
            text="Open Video",
            command=self.open_video,
            width=12
        )
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.play_button = tk.Button(
            top_frame,
            text="Play",
            command=self.play_video,
            width=10
        )
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            top_frame,
            text="Pause",
            command=self.pause_video,
            width=10
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            top_frame,
            text="Stop",
            command=self.stop_video,
            width=10
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(
            top_frame,
            text="Restart",
            command=self.restart_video,
            width=10
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.people_button = tk.Button(
            top_frame,
            text="Players: ON",
            command=self.toggle_people_detection,
            width=12
        )
        self.people_button.pack(side=tk.LEFT, padx=5)

        self.rim_button = tk.Button(
            top_frame,
            text="Rim: ON",
            command=self.toggle_rim_detection,
            width=10
        )
        self.rim_button.pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(
            top_frame,
            text="No video selected",
            anchor="w"
        )
        self.label.pack(side=tk.LEFT, padx=10)

        self.video_label = tk.Label(self.root, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)



    ##
    # @brief Opens a video file selected by the user
    #
    # @details
    # This function opens a file dialog, loads the selected video,
    # displays the first processed frame, and pauses the video
    # until the user presses play.
    #
    def open_video(self):
        file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=[
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

        self.label.config(text=os.path.basename(file_path))

        first_frame = self.video_manager.read_frame()
        if first_frame is not None:
            processed_frame = self.process_frame(first_frame)
            self.show_frame(processed_frame)

        self.video_manager.pause()



    ##
    # @brief Starts video playback
    #
    # @details
    # If no video has been loaded, a warning message is shown.
    #
    def play_video(self):
        if self.video_manager.cap is None:
            messagebox.showwarning("No Video", "Please choose a video first.")
            return

        self.video_manager.play()


    ##
    # @brief Pauses video playback
    #
    def pause_video(self):
        self.video_manager.pause()



    ##
    # @brief Stops video playback and clears the display
    #
    def stop_video(self):
        self.video_manager.stop()
        self.clear_video_display()



    ##
    # @brief Restarts the loaded video from the beginning
    #
    # @details
    # If no video has been loaded, a warning message is shown.
    #
    def restart_video(self):
        if self.video_manager.cap is None:
            messagebox.showwarning("No Video", "Please choose a video first.")
            return

        self.video_manager.restart()



    ##
    # @brief Toggles player detection on or off
    #
    # @details
    # The button text is updated to match the current detection state.
    #
    def toggle_people_detection(self):
        if self.is_processing_frame:
            return

        self.detect_people_enabled = not self.detect_people_enabled

        if self.detect_people_enabled:
            self.people_button.config(text="Players: ON")
        else:
            self.people_button.config(text="Players: OFF")



    ##
    # @brief Toggles rim detection on or off
    #
    # @details
    # The button text is updated to match the current detection state.
    #
    def toggle_rim_detection(self):
        if self.is_processing_frame:
            return

        self.detect_rims_enabled = not self.detect_rims_enabled

        if self.detect_rims_enabled:
            self.rim_button.config(text="Rim: ON")
        else:
            self.rim_button.config(text="Rim: OFF")



    ##
    # @brief Processes a single video frame
    #
    # @param frame The input video frame
    # @return The processed frame with detection boxes and labels drawn on it
    #
    # @details
    # This function detects rims and players, draws the results onto
    # the frame, and displays object counts in the top-left corner.
    #
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



    ##
    # @brief Displays a frame in the GUI window
    #
    # @param frame The frame to display
    #
    # @details
    # The frame is resized to fit inside the video display area
    # while keeping the original aspect ratio.
    #
    def show_frame(self, frame):
        display_width = self.video_label.winfo_width()
        display_height = self.video_label.winfo_height()

        if display_width < 10:
            display_width = 960
        if display_height < 10:
            display_height = 540

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_height, frame_width, _ = frame.shape
        scale = min(display_width / frame_width, display_height / frame_height)

        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)

        resized_frame = cv2.resize(frame, (new_width, new_height))

        image = Image.fromarray(resized_frame)
        self.photo = ImageTk.PhotoImage(image=image)

        self.video_label.config(image=self.photo)



    ##
    # @brief Clears the video display area
    #
    def clear_video_display(self):
        self.video_label.config(image="", bg="black")
        self.photo = None



    ##
    # @brief Continuously updates the video display
    #
    # @details
    # This function checks whether the video is playing,
    # reads the next frame, processes it, and displays it.
    # It then schedules itself to run again after a short delay.
    #
    def update_loop(self):
        if self.video_manager.is_playing:
            frame = self.video_manager.read_frame()

            if frame is not None:
                self.is_processing_frame = True
                processed_frame = self.process_frame(frame)
                self.show_frame(processed_frame)
                self.is_processing_frame = False
            else:
                self.video_manager.stop()

        delay = self.video_manager.get_delay()
        self.root.after(delay, self.update_loop)