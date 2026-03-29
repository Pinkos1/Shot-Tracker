
'''
Author: Adam Pinkos
Date: March 22nd, 2026
Brief: Simple main file to run the program

'''

import tkinter as tk
from gui import VideoPlayerGUI


def main():
    root = tk.Tk()
    app = VideoPlayerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()