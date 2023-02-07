from Data_Processors.imageProcessor import ImageProcessor
import cv2 as cv

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

    cap = cv.VideoCapture('Detection_Data/600EpochMoreDataModel/Model1_RawMatrices1.mp4')
 
 
#check if the video capture is open
if(cap.isOpened() == False):
    print("Error Opening Video Stream Or File")
 
 
while(cap.isOpened()):
    ret, frame =cap.read()
 
    if ret == True:
        cv.imshow('frame', frame)
 
        if cv.waitKey(0)  == ord('q'):
            break
 
    else:
        break
 
 
cap.release()
cv.destroyAllWindows()