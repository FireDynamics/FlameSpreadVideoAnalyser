import sys
import os
import numpy as np

import matplotlib.pyplot as plt

import cv2

# default video file name
video_fn = "warp_test.wmv"

# probe size in centimeter
target_size = (20.0, 10.0)

# number of frames to skip during the analysis
skip_frames = 10

if len(sys.argv) == 2:
    video_fn = sys.argv[1]

video = cv2.VideoCapture(video_fn)

video_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
video_nx = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
video_ny = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_dx = target_size[0] / video_nx
video_fps = video.get(cv2.CAP_PROP_FPS)

ret, frame0 = video.read()

fig, ax = plt.subplots(3, 1)
count = 0

#create output directory
output_dir_name = "output"
if not os.path.exists(output_dir_name):
    os.mkdir(output_dir_name)

# counter for progress output
frame_count_percent = 10
frame_count_group = int(video_frames * frame_count_percent / 100.0)
frame_count = frame_count_group
frame_count_output = 0

while video.isOpened():
    for i in range(skip_frames):
        ret, frame = video.read()
        count += 1

        frame_count -= 1
        if frame_count <= 0:
            frame_count = frame_count_group
            frame_count_output += frame_count_percent
            print(" {:02d}% ".format(frame_count_output))

    if ret == False:
        break

    # reverse colors of frame to RGB (OpenCV uses BGR order)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    ax[0].imshow(frame, aspect="auto", extent=[0, target_size[0], 0, target_size[1]])

    x_values = np.arange(0, target_size[0], video_dx)
    max_red = np.amax(frame[:,:,0], axis=0)
    max_green = np.amax(frame[:,:,1], axis=0)
    max_blue = np.amax(frame[:,:,2], axis=0)

    ax[1].plot(x_values, max_red, color='red', label='max red')
    ax[1].plot(x_values, max_green, color='green', label='max green')
    ax[1].plot(x_values, max_blue, color='blue', label='max blue')
    ax[1].set_xlabel("position [cm]")
    ax[1].set_ylabel("maximal")
    ax[1].set_ylim([-10,270])
    ax[1].axhline(y=0, color='grey', ls=':')
    ax[1].axhline(y=255, color='grey', ls=':')

    channel_colors = ['red', 'green', 'blue']
    for channel in range(3):

        mean = np.mean(frame[:,:,channel], axis=0)
        std = np.std(frame[:,:,channel], axis=0)

        ax[2].plot(x_values, mean, color=channel_colors[channel], linewidth=1)
        ax[2].fill_between(x_values, mean+std, mean-std, color=channel_colors[channel], alpha=0.25, linewidth=0)

    ax[2].set_ylim([-10,270])
    ax[2].axhline(y=0, color='grey', ls=':')
    ax[2].axhline(y=255, color='grey', ls=':')

    ax[2].set_xlabel("position [cm]")
    ax[2].set_ylabel("mean and stddev")


    plt.tight_layout()

    fig.savefig("{}/result_{:06d}.pdf".format(output_dir_name, count))
    ax[0].cla()
    ax[1].cla()
    ax[2].cla()

video.release()
