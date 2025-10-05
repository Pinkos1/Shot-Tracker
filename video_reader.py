##
# \file video_reader.py
# \brief Simple video playback utility using OpenCV (no detection or analysis).
# \author Adam Pinkos
# \date 5/7/25
#

import cv2

##
# \brief Reads and plays a video file at a given playback speed.
# This function opens a selected video file using OpenCV, plays it back
# in a window, and allows the user to control playback with simple keys.
#
# \param filepath Path to the video file to play.
# \param speed_factor Multiplier for playback speed (1.0 = normal speed).
#
def read_video(filepath, speed_factor=1.0):
    # Try to open the video file
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        print("Error: Cannot open video:", filepath)
        return

    # Get frames per second (FPS) and calculate frame delay in ms
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    delay = max(1, int(1000 / (fps * max(0.1, speed_factor))))  # ms between frames

    window_name = "Video Playback (ESC or Q to quit, Space to pause)"

 
    # Main video playback loop
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit when video ends

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF


        # Keyboard controls
        if key in (27, ord('q')):  # ESC or 'q' to quit
            break
        elif key == ord(' '):      # Spacebar pauses playback
            while True:
                k2 = cv2.waitKey(50) & 0xFF
                if k2 in (27, ord('q')):  # quit directly from pause
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                if k2 == ord(' '):        # resume playback
                    break

    
    
    cap.release()
    cv2.destroyAllWindows()
