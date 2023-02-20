import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

from helpers import read_video, write_video

# get our mask as a one bit np array
mask = Image.open("mask_2.png")
mask = mask.convert("1")
mask = np.array(mask)
print("opened mask")

# read video frames
frames = read_video("sdp_video_2.mp4", skip=3)
print(f"read {len(frames)} frames")
gray = [cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (5, 5), 0).astype("int16") for f in frames]

final = final_mask = np.zeros_like(gray[0])

# keep track of which pixels have changed since the beginning
# increase changed pixels by one every frame, to keep track of age
for i in range(len(frames)-1):
    delta = np.abs(gray[i] - gray[0])*mask > 10
    final_mask = delta + final_mask > 0
    final += final_mask

# make masked or unchanged pixels white
final = final.astype("float")
final[np.where(1-mask)] = np.nan
final[final == 0] = np.nan
cmap = cm.jet
cmap.set_bad('white',1.)

# plot
plt.imshow(final)
plt.show()