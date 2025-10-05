##
# \file gui.py
# \brief Minimal GUI for selecting and playing a video (no detection).
# \author Adam Pinkos
# \date 5/7/25
#

import tkinter as tk
from tkinter import filedialog, messagebox
from video_reader import read_video


##
# \brief Triggered when the "Upload & Play Video" button is clicked.
# Prompts the user to select a video file and plays it back at normal speed.
#
def upload_video():
    filepath = filedialog.askopenfilename(
        title="Select a video file",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv"), ("All Files", "*.*")]
    )
    if filepath:
        messagebox.showinfo("File Selected", f"You selected:\n{filepath}")
        read_video(filepath, speed_factor=1.0)  # Normal speed playback


##
# \brief Main window setup for the GUI.
# Creates a centered window with modern grey styling and one upload button.
#
if __name__ == "__main__":
    # Create main window
    window = tk.Tk()
    window.title("ShotTracker – Simple Video Player")
    window.configure(bg="#2e2e2e")



    # Window sizing and centering on screen
    win_width = 480
    win_height = 220
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (win_width // 2)
    y = (screen_height // 2) - (win_height // 2)
    window.geometry(f"{win_width}x{win_height}+{x}+{y}")

    # Upload button setup and styling
    upload_btn = tk.Button(
        window,
        text="Upload & Play Video",
        command=upload_video,
        font=("Helvetica", 14, "bold"),
        bg="#444444", fg="white",
        activebackground="#555555", activeforeground="white",
        relief="flat", padx=12, pady=8
    )
    upload_btn.pack(expand=True)


    window.mainloop()
