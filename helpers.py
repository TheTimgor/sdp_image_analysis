import cv2
import numpy as np
import matplotlib.pyplot as plt


# open a video file by name, pass 0 to open from camera
# skips a certain number of frames, default none
# outputs a 3D array of grayscale images
def open_video(file=0, skip=1):
    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        raise RuntimeError("Could not open video stream")  # something's gone terribly wrong!

    # read video into list
    frames = []
    count = -1  # -1 because we add before checking, and i want to include frame 0
    while cap.isOpened():
        ret, frame = cap.read()

        # only on selected frames
        count += 1
        if count % skip != 0:
            continue

        # if read correctly
        if ret:
            # just take the red channel, for better contrast
            # PLEASE find a better way of doing this later
            gray = frame[:,:,2]
            # grayscale
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # add to our array of frames
            frames.append(gray)
        else:
            # capture says we're finished reading
            break
    # np array is easier to work with
    frames = np.array(frames, dtype="int16")
    # we're done with the video stream now thank you
    cap.release()
    return frames

if __name__ == '__main__':
    frames = open_video("sdp_video_1.mp4", skip=5)
