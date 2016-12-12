import sys
import numpy as np

import cv2

# size of the final video
target_pixels = (800, 400)

# video file name
video_fn = "test.wmv"

# number of frames to skip with space
skip_size = 10

source_corners = []
target_corners = [[0,0], [0, target_pixels[1]], [target_pixels[0], target_pixels[1]], [target_pixels[0], 0]]

def mouse_four_corners(event, x, y, d1, d2):
    global source_corners, frame0

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    # print("mouse click at ", x, y)

    source_corners.append([x,y])

    cv2.circle(frame0, (x,y), 10, (255,0,0), 2)

if len(sys.argv) == 2:
    video_fn = sys.argv[1]

video = cv2.VideoCapture(video_fn)

ret, frame0_raw = video.read()

frame0 = np.copy(frame0_raw)

cv2.namedWindow("first frame", cv2.WINDOW_AUTOSIZE)
cv2.imshow("first frame", frame0)

cv2.setMouseCallback("first frame", mouse_four_corners)

while True:
    key=cv2.waitKey(1)
    cv2.imshow("first frame", frame0)

    # enter -> warp movie
    if key==13: break

    # esc -> restart
    if key==27:
        source_corners = []
        frame0 = np.copy(frame0_raw)

    # space -> move 100 frames forward
    if key==32:
        for i in range(skip_size):
            ret, frame0_raw = video.read()
        frame0 = np.copy(frame0_raw)
        source_corners = []

cv2.destroyWindow("first frame")

# print(source_corners)

h, status = cv2.findHomography(np.array(source_corners), np.array(target_corners))

frame0_warp = cv2.warpPerspective(frame0_raw, h, target_pixels)

cv2.namedWindow("first frame warped", cv2.WINDOW_AUTOSIZE)
cv2.startWindowThread()
cv2.imshow("first frame warped", frame0_warp)

while True:
    key=cv2.waitKey(1)
    if key==27: sys.exit(1)
    if key==13: break

cv2.destroyWindow("first frame warped")
cv2.waitKey(1)

result = cv2.VideoWriter("warp_{}".format(video_fn), cv2.VideoWriter_fourcc(*'XVID'), 24, target_pixels)

video_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

# rewind video
video.set(cv2.CAP_PROP_POS_FRAMES, 0)

# counter for progress output
frame_count_percent = 10
frame_count_group = int(video_frames * frame_count_percent / 100.0)
frame_count = frame_count_group
frame_count_output = 0

print("processing movie: \n 00% ")

while video.isOpened():
    ret, frame = video.read()
    if ret == False: break

    frame_warp = cv2.warpPerspective(frame, h, target_pixels)

    result.write(frame_warp)

    frame_count -= 1
    if frame_count <= 0:
        frame_count = frame_count_group
        frame_count_output += frame_count_percent
        print(" {:02d}% ".format(frame_count_output))

video.release()
result.release()