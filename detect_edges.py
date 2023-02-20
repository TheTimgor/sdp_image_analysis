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

# read video frames
SKIP_FRAMES = 3
frames = read_video("sdp_video_2.mp4")
frames = frames[::SKIP_FRAMES]
print(f"read {len(frames)} frames")


# run edge detection on each frame
edges = [cv2.Canny(f, 80, 110) for f in frames]
edges_masked = [e*mask for e in edges]
print("finished edge detection")


# invert, convert to BGR
edges_video = np.array([np.repeat(255-e[:, :, None], 3, axis=2) for e in edges_masked])
# generating final output video
video_width = edges[0].shape[1]
video_height = edges[0].shape[0]
video_frames = len(edges)
output_video = []


# calculate number of pixels changed from the beginning
# this is a proxy for displaced volume
frame_0 = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY).astype("int16")
deltas = [np.sum(np.abs(frame_0-cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))*mask > 10) for f in frames]
print("calculated deltas")

# calculate edge lengths
# this is a proxy for contact line length
edge_lengths = [np.sum(e)/255 for e in edges_masked]
print("calculated edge lengths")


# preapre stuff for plotting
# updating the line data directly is faster than making a new plot, but the code is a bit contrived
fig = plt.figure(figsize=(8, 16*video_height/video_width), dpi=video_width/16)
ax = fig.subplots(2)
#
ax[0].set_xlim([0, len(deltas)])
ax[0].set_ylim([0, max(deltas)])
ax[0].set_title("Displaced area")
data0 = [None]*video_frames
line0, = ax[0].plot(data0)

ax[1].set_xlim([0, len(edge_lengths)])
ax[1].set_ylim([0, max(edge_lengths)])
ax[1].set_title("Contact line length")
data1 = [None]*video_frames
line1, = ax[1].plot(data1)


# generate the final video
for i in range(video_frames):
    # update plots
    data0[:i+1] = deltas[:i+1]
    line0.set_ydata(data0)
    data1[:i+1] = edge_lengths[:i+1]
    line1.set_ydata(data1)
    fig.canvas.draw()
    # get canvas as RGB and then convert to BGR
    plot = np.asarray(fig.canvas.buffer_rgba())[:, :, 2::-1]
    # add quadrants together, halving where necessary
    frame = np.append(
        np.append(frames[i][::2, ::2, :], edges_video[i][::2, ::2, :], axis=0),
        plot,
        axis=1)
    output_video.append(frame)


# save everything to disk
# disk? really? what year is it? can you even BUY laptops with HDDs anymore?
write_video("output.mp4", edges_video, 30/SKIP_FRAMES)
write_video("combined_output.mp4", output_video, 30/SKIP_FRAMES)
print("finished writing video")
