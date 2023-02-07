## Creates video from a set of images
## Used to validate the model

import cv2 as cv
import numpy as np
import glob
import os
import natsort

if __name__ == "__main__":
    img_array = []

    current_dir = os.getcwd()
    matrix_dir = current_dir + '/Processed_Data/Model1_TestingSetDupe/images'
    for filename in natsort.natsorted(glob.glob(matrix_dir + '/*.jpg')):
        img = cv.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv.VideoWriter('Matrix_Videos/Model1_RawMatrices1.mp4', 0x7634706d, 60, (width, height))

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()