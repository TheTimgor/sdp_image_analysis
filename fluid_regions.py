import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from helpers import read_video, write_video

# get our mask as a one bit np array
mask = Image.open("mask_2.png")
mask = mask.convert("1")
mask = np.array(mask)
print("opened mask")

frames = read_video("sdp_video_2.mp4", skip=200)
frames = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]
print(f"read {len(frames)} frames")
VIDEO_WIDTH = frames[0].shape[1]
VIDEO_HEIGHT = frames[0].shape[0]

# colors of oil and nf. tiled to the size of image for easy computation
color_1 = np.tile((73, 135, 190), (VIDEO_HEIGHT, VIDEO_WIDTH, 1))
color_2 = np.tile((15, 115, 155), (VIDEO_HEIGHT, VIDEO_WIDTH, 1))

for f in frames:
    blur = cv2.GaussianBlur(f, (3, 3), 0)

    grad_x = cv2.Sobel(blur, -1, 1, 0)
    grad_x = cv2.GaussianBlur(grad_x, (9, 9), 0)
    grad_x = (grad_x < 10) * grad_x

    grad_y = cv2.Sobel(blur, -1, 0, 1)
    grad_y = cv2.GaussianBlur(grad_y, (9, 9), 0)
    grad_y = (grad_y < 10) * grad_y


    fig, ax = plt.subplots(2, 2)
    ax[0, 0].imshow(f)
    ax[1, 0].imshow(grad_x)
    ax[1, 1].imshow(grad_y)
    plt.show()

