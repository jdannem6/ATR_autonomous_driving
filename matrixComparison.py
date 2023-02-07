from Data_Processors.imageProcessor import ImageProcessor
import cv2 as cv
import numpy as np

if __name__ == "__main__":
    # Create ImageProcessor
    imageProcessor = ImageProcessor()
 
    # current_dir = os.getcwd()
    # print(current_dir)
    # # Create the VideoCapture and set the imageProcessor object to stream from it
    # capture = cv.VideoCapture(current_dir + '/Model3Labeled1.mp4')
    # imageProcessor.setVideoStream(capture)

    # # Change to MatrixStorage directory to store the image matrices there
    # directory = r'/home/jdannem6/opencv/Gamepad/MatrixStorage'
    # os.chdir(directory)

    # # Get Next Image Matrix
    # nextMatrix = 0
    # matrixIndex = 0
    # while (nextMatrix is not None):
    #     nextMatrix = imageProcessor.nextImageMatrix()
    #     if nextMatrix is not None:
    #         # Extract the image matrix from the object and store it ina file
    #         # fileName = "Matrix" + str(matrixIndex) + ".jpg"
    #         # #next = nextMatrix.getImageMatix()
    #         # cv.imwrite(fileName, nextMatrix.getImageMatix())
    #         # Increment matrix index after each matrix printed
    #         matrixIndex += 1

    #         # # Extract timestamp information
    #         # timestamps = nextMatrix.getTimestamps()

    #         # # Request control data segement around each timestamp
    #         # windowSize = 50
    #         # for timestamp in timestamps:
    #         #     # Define lowerBound and upper bound of time interval for control
    #         #     # data
    #         #     lowerBound = timestamp - int(windowSize/2)
    #         #     upperBound = timestamp + windowSize/2
    #         #     # Define corresponding time interval
    #         #     timeInterval = [lowerBound, upperBound]
    #         #     # Request control data occurring within timeInterval
    #         #     controlDataBlock = getDataInInterval(timeInterval)

    cap1 = cv.VideoCapture('Detection_Data/800EpochModel/Model1_RawMatrices1.mp4')
    cap2 = cv.VideoCapture('Detection_Data/600EpochModel/Model1_RawMatrices1.mp4')
    cap3 = cv.VideoCapture('Detection_Data/600EpochMoreDataModel/Model1_RawMatrices1.mp4')
    cap4 = cv.VideoCapture('Detection_Data/700EpochModel/Model1_RawMatrices1.mp4')
 
 
#check if the video capture is open
if(cap1.isOpened() == False or cap2.isOpened() == False):
    print("Error Opening Video Stream Or File")
    exit()
 
i = 0
while(cap1.isOpened() and cap2.isOpened()):
    ret1, frame1 =cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()
 
    if ret1 == True and ret2 == True:
        # Combine frames
        combinedFrame = np.concatenate((frame1, frame2), axis=1)
        combinedFrame = np.concatenate((combinedFrame, frame3), axis=1)
        combinedFrame = np.concatenate((combinedFrame, frame4), axis=1)

        cv.imshow('frame', combinedFrame)
 
        if cv.waitKey(0)  == ord('q'):
            break
 
    else:
        break
    print(i)
    i+=1
 
cap1.release()
cap2.release()
cap3.release()
cv.destroyAllWindows()