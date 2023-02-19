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
print(f"read {len(frames)} frames")

f = frames[1]
output_video = []

for gap in range(0, 200, 10):
    for thresh in range(0, 200, 10):
        edge = 255-cv2.Canny(f, thresh, thresh+gap)*mask
        edge = np.repeat(edge[:, :, None], 3, axis=2)
        edge = cv2.putText(edge, f"lower {thresh} upper {thresh+gap}", (50, 2150), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0))
        output_video.append(edge)

write_video("calibration.mp4", output_video, 5)
print("finished writing video")

