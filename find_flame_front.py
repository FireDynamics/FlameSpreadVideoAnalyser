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

# set color channel to show as top image
color_channel = 1

# define how to analyse a line tangential to the flame spread, output must be a single number
# line has the type: (ny, 3), where ny is the number of pixels and 3 is the number of color channels
def analyse_line(line):

    # determine the maximal value of the second (index 1) color channel, here green
    max_green = np.max(line[:,1])
    max_red= np.max(line[:,0])
    max_blue= np.max(line[:,2])
    
    max_farben= max(max_blue, max_red, max_green)
    
    
    return max_farben

# define how to process the values got for each line by the function 'analyse_line' to find the flame front
# line_values is a simple numpy array with the shape (nx)
def analyse_front(line_values):

    # find all indeces where the values of line_values are bigger than 250
    pos = np.where(line_values > 250)

    # if there are no such indeces, set the flame position to zero
    if len(pos[0]) == 0:
        pos = 0
    # otherwise take the last index
    else:
        pos = pos[0][-1]

    return pos


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

total_result = []
old_pos = 0

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

    line_values = np.zeros(video_nx)
    # call for each line the line analyser
    for ix in range(video_nx):
        line_values[ix] = analyse_line(frame[:, ix, :])

    # call function to analyse all line values
    pos = analyse_front(line_values)
    pos = pos * video_dx

    if old_pos > pos:
        pos = old_pos

    old_pos = pos

    time = count / video_fps

    ax[0].imshow(frame[:,:,color_channel], cmap=plt.get_cmap("afmhot"), aspect="auto", extent=[0, target_size[0], 0, target_size[1]])
    ax[0].axvline(x=pos, color='b')

    ax[1].plot(np.arange(0, target_size[0], video_dx), line_values)
    ax[1].set_xlabel("position [cm]")
    ax[1].set_ylabel("line value []")
    ax[1].set_ylim([0,255])

    ax[2].scatter(time, pos)
    ax[2].set_xlim([0, video_frames / video_fps])
    ax[2].set_ylim([0, target_size[0]])
    ax[2].set_ylabel("flame position [cm]")
    ax[2].set_xlabel("time [s]")

    plt.tight_layout()

    fig.savefig("{}/result_{:06d}.pdf".format(output_dir_name, count))
    ax[0].cla()
    ax[1].cla()
    # ax[2].cla()

    total_result.append([time, pos])


video.release()

fout = open("output/results.csv", 'w')
fout.write("# time [s]; position [cm]\n")
for res in total_result:
    fout.write("{}; {}\n".format(res[0], res[1]))
fout.close()
