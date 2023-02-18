import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def get_edges(file=0, skip=1):
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
            # canny edge detection, parameters threshold and dy need to be tweaked manually
            edges = cv2.Canny(frame, 100, 200)
            frames.append(edges)
        else:
            # capture says we're finished reading
            break
    # np array is easier to work with
    frames = np.array(frames, dtype="int16")
    # we're done with the video stream now thank you
    cap.release()
    return frames


if __name__ == "__main__":
    # get our mask as a one bit np array
    mask = Image.open("mask_2.png")
    mask = mask.convert("1")
    mask = np.array(mask)

    edges = get_edges("sdp_video_2.mp4", skip=100)

    fig, ax = plt.subplots(1,2)
    for e in edges:
        ax[0].imshow(e)
        ax[1].imshow(e*mask)
        plt.show()
