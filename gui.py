
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