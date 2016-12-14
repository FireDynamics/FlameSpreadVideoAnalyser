Tool to analyse video data of flame spread. It mainly consists of two steps: a) warp perspective video into an orthogonal view and b) analyse the warped video.

Both tools need the opencv python modules to be installed.

Both scripts are written for python 3.

Together with the sample movie file, both scripts should run without issues with the default values.

## How to use warp_movie.py

1. adopt the target video resolution (default `target_pixels = (800,400)`)
1. adopt video file name (default `video_fn = "test.wmv"`) or pass the file name as first command line argument
1. once invoked, a window opens and shows the first frame with following user interactions
 * mark four corners with a mouse click (positions are indicated with blue circles) in the following order: top-left -> bottom-left -> bottom->rigth -> top-right
 * to flip the target movie, swap either top/bottom or left/right
 * to restart the corner selection process, press 'esc'
 * to move 10 frames forward, press 'space', there is no option to go back, this value may be changed with `skip_size`
 * to proceed further, press 'enter'
1. a control image of the warped selected frame is shown, if it is ok, press 'enter' to start the movie convertion, to stop the process, press 'esc'
1. the converted new movie has *warp_* prepended to the original movie file name, the original file should not be overwritten

## How to use find_flame_front.py

1. adopt the target physical extension in cm (default `target_size = (20,10)`)
1. adopt video file name (default `video_fn = "test.wmv"`) or pass the file name as first command line argument
1. adopt the number of frames to be skipped during the analysis (default `skip_frames=10`)
1. define both analysis functions: `analyse_line` and `analyse_front`, see inline documentation on the functions template
1. run the script, the output will be placed in the `output` folder
1. all created pdf and a result file `results.cvs`, that contains a table time [s] vs. flame position [cm], are placed in the `output` folder
