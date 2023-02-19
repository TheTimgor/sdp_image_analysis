import cv2


# open a video file by name, pass 0 to open from camera
# skips a certain number of frames, default none
# outputs a 3D array of grayscale images
def read_video(file=0, skip=1):
    cap = cv2.VideoCapture(file)
    if not cap.isOpened():
        raise RuntimeError("Could not open read video stream")  # something's gone terribly wrong!

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
            frames.append(frame)
        else:
            # capture says we're finished reading
            break
    # we're done with the video stream now thank you
    cap.release()
    return frames


# save frames of video to avi file
def write_video(file, frames, fps=30):
    # create a video writer
    size = (frames[0].shape[1], frames[0].shape[0])
    out = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)

    if not out.isOpened():
        raise RuntimeError("Could not open write video stream")  # something's gone terribly wrong!

    # work through all our frames and yeet them at the writer
    for frame in frames:
        out.write(frame)
    out.release()
    return frames


# simple test
if __name__ == '__main__':
    video = read_video("sdp_video_1.mp4", skip=10)
    write_video("out.mp4", video, fps=5)

