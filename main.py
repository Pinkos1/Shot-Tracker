##
# @file main.py
# @author Adam Pinkos
# @date March 22, 2026
# @brief Simple main file to run the program
#
# @details
# This file serves as the entry point for the shot tracker application.
# It initializes the GUI and starts the main event loop.
#

import tkinter as tk
from gui import VideoPlayerGUI



##
# @brief Entry point for the Shot Tracker application
#
# @details
# - Creates the main GUI window using Tkinter
# - Instantiates the VideoPlayerGUI class
# - Runs the application until the window is closed
#
def main():
    root = tk.Tk()
    app = VideoPlayerGUI(root)
    root.mainloop()



##
# @brief Runs the program if executed as a script
#
#
if __name__ == "__main__":
    main()