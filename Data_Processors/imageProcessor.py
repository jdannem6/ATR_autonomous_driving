# coding: utf-8

# Image Processing Pipeline
# Part of the Driving Control Prediction Project
# Written by Justin Dannemiller
# Last Edited 6/2/2022

# This file defines the methods and attributes of the imageProcessor class, 
# the class used to create NxM image matrices from a video stream

# Still need to set up timestamp queue within the ImageProcessor Class
# We also need to figure out how to set up timestamp extraction from frames and
# how to synchronize these time frames with those of the control processor
# I'm thinking of creating a main program which creates a control processor and
# a image processor. 
# When each of those objects are created, they set their firstTimestamp to the 
# current time, thereby creating what should be approximately a shared constant

# Notes:
""" The Image Queue was implemented using a list as opposed to a queue
Even though implementing it with a queue data structure would be more 
efficient during updates (O(1) vs O(n)), printing the image Matrix would be 
O(n) for both implementations and would require the creation of a copy of 
the queue which could be costly since it contains images """

""" New additions to implement into program
1. Add frame skipping for modification of duration of memories
2. Reverse order of Matrix
3. Test validity of matrix structure with different sizes
4. Attempt with live streams
"""
#import Gamepad
from threading import current_thread
import numpy as np
#from AsyncExample import getDataInInterval
#from AsyncExample import getLowerIndex
import cv2 as cv
import os
import time # Necessary for timestamps
import json
import glob # Needed for glob.glob which allows fetching of filenames in directory
# Maybe we add some functions later that allow resetting the the image matrix 
# or timestamps stored in the image matrix object

# Stores a frame from the video capture and its corresponding timestamp
class Frame:
    def __init(self, image, timestamp):
        self.__image = image
        self.__timestamp = timestamp
    
class ImageMatrix:
    def __init__(self, image, timestamps):
        self.__imageMatrix = image
        self.__timestamps = timestamps
    # Returns a collection of timestamps corresponding to the collection of 
    # frames stored within the ImageMatrix
    def getTimestamps(self):
        timestampList = []
        # Return list of all timestamps in data matrix
        i = 0
        for timestamp in self.__timestamps:
            timestampList.append(timestamp)
        return timestampList
    # Returns the image matrix stored in the imageMatrix object
    def getImageMatrix(self):
        return self.__imageMatrix

# Class used to produce Image Matrices from a provided video stream
class ImageProcessor:
    def __init__(self, resolution=(608, 608), dimensions=(3,3), videoStream=None, imageDirectory=None, framesToSkip = 8):
        # Set the initialization timestamp
        self.__firstTimestamp = time.time()

        # Initialize the desired dimensions of the image Matrices. 
        self.__rowCount = dimensions[0] # Number of rows in matrix
        self.__columnCount = dimensions[1] # Number of columns in matrix

        # Initialize frame index for accessing frames in raw storage
        self.__frameIndex = 0
        # Initialize the desired resolution of the frames
        # Each frame has 1/M the width and 1/N the height of the
        # Image Matrix containing it
        self.__frameWidth = int(resolution[0] / self.__columnCount)
        self.__frameHeight = int(resolution[1] / self.__rowCount)

        # Initialize framesToSkip parameter (determines how many many frames
        # are skipped between each pair of sequential frames in image matrix)
        self.__framesToSkip = framesToSkip

        self.__videoStream = videoStream

        # Initialize the image directory such that the image processor can
        # find the raw images to process
        self.__imageDirectory = imageDirectory
        # Initalize the list of image files in imageDirectory
        self.__listofImageFiles = []
        # Unless otherwise specified, the image Processor does not use a image Directory
        # to store its frames
        self.__usesImageDirectory = False

        # Image Queue initially stores NxM black images
        self.__imageQueue = []

        # Dicitonary to store unprocessed frames
        self.__rawFrameStorage = [] # Dictionary to store raw frames
        # Creates black image
        # blackImage = np.zeros((self.__frameWidth, self.__frameHeight, 3), np.uint8)
        # i = 0
        # # Insert NxM black images into the image Queue
        # while (i < self.__rowCount * self.__columnCount):
        #     self.__imageQueue.append(blackImage)
        #     i+=1

        # Timestamp queue intially stores NxM copies of -1 timestamp (one for 
        # each black image)
        self.__timestampQueue = []
        # i = 0
        # blackTimestamp = -1
        # while (i < self.__rowCount * self.__columnCount):
        #     self.__timestampQueue.append(blackTimestamp)
        #     i+=1
    # Returns the playback rate in FPS of video stream
    def getPlaybackRate(self):
        return self.__videoStream.get(cv.CAP_PROP_FPS)
    # Plays the video frame-by-frame by displaying its frames at their
    # native frame rate. This function was used for logically demonstrating
    # the effectiveness of our model
    def showVideo(self):
        # Return error if the video stream has not yet been properly set
        if (self.__videoStream == None):
            print("Error: video stream must be established prior to showing its contents!")
            exit(1)
        # Otherwise, show the video
        else:
            isLastFrame = False
            frameIndex = 0
            numberOfFrames = len(self.__rawFrameStorage)
            while(frameIndex < numberOfFrames):
                nextFrameObject = self.__rawFrameStorage[frameIndex]
                nextFrame = nextFrameObject['frame']
                frameIndex < numberOfFrames
                cv.imshow("Original Video", nextFrame)
                cv.waitKey(cv.CAP_PROP_FPS)
                frameIndex += 1
    # Reads frames, displays them, and stores them in folder for later processing
    # If isVideoStream is True, 
    def readFrames(self, isVideoStream):
        # Return error if the video stream has not been properly set
        if self.__videoStream == None:
            print("Error: video stream must be established prior to processing images")
            exit(1)
        # Get next frame
        frameWasReturned = True
        while (frameWasReturned is True):
            frameWasReturned, frame = self.__videoStream.read()
            # If frame was returned, store it in the RawImageDirectory
            if (frameWasReturned):
                # Get current timestamp for filename
                timestamp = time.time() - self.__firstTimestamp
                timestamp = int(timestamp * (1000)) # Express timestamp in ms

                # Name file with current timestamp
                filename = "frame" + str(timestamp)

                # Define the frame JSON object
                frameObject = {
                    "timestamp": timestamp,
                    "frame": frame
                }
                # Show the frame
                cv.imshow("Original Video", frame)
                # Get in milliseconds time between frames
                timeBetweenFrames = int(1000*1/self.__videoStream.get(cv.CAP_PROP_FPS))
                cv.waitKey(timeBetweenFrames)

                # Add the next frame to the frame dictionary
                self.__rawFrameStorage.append(frameObject)
        # Serialize storage of frames
        #serializedFrames = json.dumps(self.__rawFrameStorage, indent = 4)
        # Write to json file
        #with open("RawImageData.json", "w") as RawImageData:
            #rawImageData.write(serializedFrames)




    # Returns the value of the saved timestamp
    def getFirstTimestamp(self):
        return self.__firstTimestamp

    # Sets the value of the resolution of the image Matrix
    def setResolution(self, resolution):
        self.__frameWidth = resolution[0]
        self.__frameHeight = resolution[1]

    # Changes the value of the frameIndex
    def setFrameIndex(self, newIndexValue):
        self.__frameIndex = newIndexValue
    # Returns the current value of the frame Index
    def getFrameIndex(self):
        return self.__frameIndex

    # Sets the dimensions of the Image Matrices produced by instances of the 
    # class
    def setMatrixDimensions(self, dimensions):
        self.__rowCount = dimensions[0]
        self.__columnCount = dimensions[1]

    # Sets the video stream of the image processor, allowing it to process images
    # obtained from that stream
    def setVideoStream(self, videoCaptureStream):
        # Consider adding some type checking code here
        self.__videoStream = videoCaptureStream

        # Set the scaling factors using the width and height of the 
        # the stream's frames
        prevFrameWidth = self.__videoStream.get(cv.CAP_PROP_FRAME_WIDTH)
        prevFrameHeight = self.__videoStream.get(cv.CAP_PROP_FRAME_HEIGHT)
        # Scaling factors are (desired Frame dimensions)/(previous frame dim)
        self.__widthScalingFactor = self.__frameWidth / prevFrameWidth
        self.__heightScalingFactor = self.__frameHeight / prevFrameHeight

    # Set the imageDirectory of the image processor allowing it to take raw images
    # from a given directory and process them. imageDirectory is used in place
    # of video stream when the raw images are already captured and timestampped
    def setImageDirectory(self, imageDirectory):
        # Ensure all images within the image directory can be opened
        try:
            # Try to read each file
            for filename in glob.glob(imageDirectory + '/*.jpg'):
                image = cv.imread(filename)
                # Try to get properties of the image. *This will error out if image
                # couldn't  be read*
                height, width, layers = image.shape
        except Exception as e:
            # Print the error message
            print(e)
        
        # If the program didn't error out, set the image directory to read images
        # from, set usesImageDirectory to true, and initialize the list of 
        # image files
        self.__imageDirectory = imageDirectory
        self.__usesImageDirectory = True
        # Retrieve all filenames of raw image files
        unsortedListOfFiles = glob.glob(self.__imageDirectory + '/*.jpg')
        # Sort and then save the list
        self.__listofImageFiles = sorted(unsortedListOfFiles)


    def printImageNames(self):
        i = 0
        print("Filenames in Order")
        while i < 200:
            print("File " + str(i) + self.__listofImageFiles[i])
            i+=1

    # Future change: Currently, this class stores the video stream, but we could
    # alternatively store the video stream outside this class and pass frames to it
    
    # Returns the next frame to be inserted into the queue. Takes as input, the image
    # processor object (implicitly), the the number of frames to skip between each pair
    # of selected frames
    def selectNextFrame(self, framesToSkip):
        # Get the index of the next frame to process
        startingIndex = self.__frameIndex
        currentIndex = startingIndex
        # If usesImageDirectory is true, select next frame from image directory
        if (self.__usesImageDirectory):
            # Return none if the requested frame does not exist
            totalNumOfFrames = len(self.__listofImageFiles)
            # If the number of frames to skip exceeds the number of 
            # frames remaining, the requested frame does not exist
            requestedFrameIndex = startingIndex + framesToSkip
            if (requestedFrameIndex > (totalNumOfFrames - 1)):
                return None

            # Otherwise, find the requested frame
            else:
                requestedFilePath = self.__listofImageFiles[requestedFrameIndex]
                requestedFrame = cv.imread(requestedFilePath)

                ## Get the frame's timestamp from its filename
                # Get file name (occurs after the last forward slash in path)
                requestedFileName = requestedFilePath.split('/')[-1]
                # Timestamp listed after the occurence of word "image" and
                # before the .jpg file extension
                timestampWithFileExt = requestedFileName.split("image")[-1]
                timestamp  = timestampWithFileExt.split('.jpg')[0]
                # Convert timestamp to integer
                timestamp = float(timestamp)
                ## Create a JSON frame object to store the frame and its timestamp
                frameObject = {
                    "timestamp": timestamp,
                    "frame": requestedFrame
                }
                return frameObject
        # Otherwise, select next frame from the raw frame storage
        else:
            # Otherwise, keep reading frames until the (framesToSkip + 1)th frame has been
            # reached
            startingIndex = self.__frameIndex
            currentIndex = startingIndex
            # Return none if requested frame does not exist
            numberOfFrames = len(self.__rawFrameStorage)
            if ((numberOfFrames - 1) - startingIndex < framesToSkip):
                return None
            else:
                while (currentIndex < startingIndex + framesToSkip):
                    frameObject = self.__rawFrameStorage[currentIndex] # Get next frame
                    currentIndex += 1 
                # Return the (framesToSkip + 1)th frame
                return frameObject


    # Creates and returns a frame object containing the nth image in the 
    # videostream or image directory and the timestamp at which it was 
    # captured
    def __selectNthFrame(self, desiredFrameIndex):

        # If usesImageDirectory is true, select next frame from image directory
        if (self.__usesImageDirectory):
            # Return none if the requested frame does not exist
            lastFrameIndex = len(self.__listofImageFiles) - 1

            ## If there exists no frame with the given index, return none  for frame object
            """ Make this set a boolean later that indicates that the last frame has
                been reached and use this in the loop that requests the image matrices"""
            if (desiredFrameIndex > lastFrameIndex):
                print("Requested Index is out of range!")
                return None

            ## Otherwise, if there is such a frame, try to retrieve it
            else:
                # If raw images stored in raw image directory, obtain image file path from list
                if (self.__usesImageDirectory):
                    frameFilePath = self.__listofImageFiles[desiredFrameIndex]
                    # Try to read corresponding image
                    frame = cv.imread(frameFilePath)
                    # Return None and error message if couldn't be read
                    if (frame.size == 0): 
                        print("Error: The " + str(desiredFrameIndex) + "th frame could not be opened!")
                        return None
                    # Otherwise, produce an image matrix containing the given frame
                    else:
                        ## Get the timestamp corresponding to the frame from the filename
                        frameFileName = frameFilePath.split('/')[-1]
                        # By convention, the timestamp is listed after the word image 
                        # and before the .jpg file extension
                        timestamp = frameFileName.split('image')[-1].split('.jpg')[0]
                        timestamp = float(timestamp) # Convert timestamp to float

                        ## Create at JSON frame object to store the frame and its timestamp
                        frameObject = {
                            "timestamp": timestamp,
                            "frame": frame
                        }
                        return frameObject
        # Otherwise, if the frame is to be selected from raw frame storage
        else:
            # Otherwise, keep reading frames until the (framesToSkip + 1)th frame has been
            # reached
            startingIndex = self.__frameIndex
            currentIndex = startingIndex
            # Return none if requested frame does not exist
            lastFrameIndex = len(self.__rawFrameStorage)
            if (desiredFrameIndex > lastFrameIndex):
                return None
            else:
                return frameObject

    # Produces and returns the next image matrix. This is performed by taking 
    # the next frame from the video stream, inserting it into the queue, 
    # removing the earliest-added frame, and formatting the queue's contents
    # into a NxM image matrix
    def nextImageMatrix(self):
        # Return error if the video stream has not been properly set
        if self.__videoStream == None and self.__usesImageDirectory == False:
            print("Error: video stream must be established prior to processing images")
            exit(1)
        # Otherwise, read the next frame
        # Otherwise, process the next ImageMatrix
        else:
            framesToSkip = 8

            """ This needs to be changed later because framesToSkip is a parameter that should never change
                during the execution of the program. Due to this, it should be a member of the ImageProcessor
                class and not a parameter passed to the selectNextFrame function """
            frameObject = self.selectNextFrame(framesToSkip) 
 

            # If last frame has been reached, give an error message and return
            if (frameObject is None):
                print("Last Frame has been reached")
                return None
            # Otherwise, use the frame to make the next image matrix
            else:
                nextFrame = frameObject['frame']
                # Update Frame Index to reflect the framesToSkip frames skipped
                self.setFrameIndex(self.getFrameIndex() + framesToSkip)
                # Increment the index for the next frame selection
                ## Resize the next frame
                # Desired frame dimensions
                frameDimensions = (self.__frameWidth, self.__frameHeight)
                resizedFrame = cv.resize(nextFrame, frameDimensions, interpolation= cv.INTER_AREA )

                # Insert new, resized frame
                self.__imageQueue.append(resizedFrame)
                # Remove earliest added frame
                self.__imageQueue.pop(0)

                """ For now, the timestamps are not relative to the video. In 
                other words, I am simply using setting the timestamps to the current
                time. In doing so, they may depend a bit on computational speeds. Later
                we might consider using frame time information to set timestamps """
                # Add new timestamp to queue
                timestamp = frameObject['timestamp']
                self.__timestampQueue.append(timestamp)
                # Remove earliest added timestamp from the queue
                self.__timestampQueue.pop(0)



                # Create an Image Matrix containing the contents of the image queue
                i, j = self.__rowCount - 1, self.__columnCount - 1
                while (i >= 0):
                    j = self.__columnCount -1
                    while(j >= 0):
                        # Calculate one-dimensional index of frame within imageQueue
                        frameIndex = (i* self.__rowCount) + j
                        # Get corresponding frame
                        frameToPrint = self.__imageQueue[frameIndex]
                        # Append that frame to the row
                        if (j == self.__columnCount - 1): 
                            rowOfFrames = frameToPrint
                        else:
                            rowOfFrames = np.concatenate((rowOfFrames, frameToPrint), axis = 1)
                            #image_row = np.concatenate((image_row, resized_frame), axis = 1)
                        j-=1
                    # After row of images has been created. Append it to the Image Matrix
                    if (i == self.__rowCount - 1):
                        imageMatrix = rowOfFrames
                    else:
                        imageMatrix = np.concatenate((imageMatrix, rowOfFrames), axis = 0)
                    i-=1

                # Print and return the resulting Image Matrix
                cv.imshow("Image Matrix", imageMatrix)
                # Create the next ImageMatrix object
                imageMatrix = ImageMatrix(imageMatrix, self.__timestampQueue)
                # Wait for keyboard input
                cv.waitKey(0)
                return imageMatrix

        
    # Produces and returns the next image matrix. This is performed by taking 
    # the next frame from the video stream, inserting it into the queue, 
    # removing the earliest-added frame, and formatting the queue's contents
    # into a NxM image matrix
    def nextImageMatrix2(self):
        # Return error if the video stream has not been properly set
        if self.__videoStream == None and self.__usesImageDirectory == False:
            print("Error: video stream must be established prior to processing images")
            exit(1)
        # Otherwise, process the next image matrix
        else:
            self.__imageQueue.clear()
            self.__timestampQueue.clear()
            # Get the first frame in the image matrix
            frameObject = self.__selectNthFrame(self.__frameIndex)

            # If a frame was not successfully retrieved, return None for the 
            # image matrix object and print an error message
            if (frameObject == None):
                missingMatrixErrorMessage = "Could not produce the next image matrix. \
                                The last frame may have been reached! "
        
                print(missingMatrixErrorMessage)
                return None
            ### Otherwise, process the frame
            else:
                firstFrameInMatrix = frameObject['frame']
                ## Resize the frame
                frameDimensions = (self.__frameWidth, self.__frameHeight)
                resizedFrame = cv.resize(firstFrameInMatrix, frameDimensions, interpolation = cv.INTER_AREA)

                # Insert resized frame into the image queue for later processing
                self.__imageQueue.append(resizedFrame)
                # Insert frame's timestamp into timestamp queue
                frameTimestamp = frameObject['timestamp']
                self.__timestampQueue.append(frameTimestamp)

                # Process the other (n * m) - 1 frames that comprise the 
                # remainder of the image matrix
                remainingFrameCount = self.__rowCount * self.__columnCount - 1
                previousFrameIndex = self.getFrameIndex()
                while (remainingFrameCount > 0):
                    # Get the previous frame (frame that occurs framesToSkip frames before
                    # the last retrieved frame
                    previousFrameIndex = previousFrameIndex  - self.__framesToSkip

                    # If the index of previous frame is negative, frame doesn't exist. 
                    # Substitute black image in its place
                    if (previousFrameIndex < 0):
                        blackImage = np.zeros((self.__frameWidth, self.__frameHeight, 3), np.uint8)
                        previousFrame = blackImage
                    # Otherwise, try to retrieve that frame
                    else:
                        previousFrameObject = self.__selectNthFrame(previousFrameIndex)
                        # If frame could not be retrieved, give error message and exit
                        if (previousFrameObject == None):
                            print("Requested frame could not be retrieved. Exiting...")
                            exit(1)
                        # Otherwise, extract process the image
                        else:
                            previousFrame = previousFrameObject['frame']
                            ## Resize the frame
                            frameDimensions = (self.__frameWidth, self.__frameHeight)
                            previousFrame = cv.resize(previousFrame, frameDimensions, interpolation = cv.INTER_AREA)

                    # Insert frame into the image queue for later processing
                    self.__imageQueue.append(previousFrame)
                    remainingFrameCount = remainingFrameCount - 1

                # Create an Image Matrix containing the contents of the image queue
                i = 0
                while (i < self.__rowCount):
                    j = 0
                    while(j < self.__columnCount):
                        # Calculate one-dimensional index of frame within imageQueue
                        frameIndex = (i* self.__rowCount) + j
                        # Get corresponding frame
                        frameToPrint = self.__imageQueue[frameIndex]
                        # Append that frame to the row
                        if (j == 0): 
                            rowOfFrames = frameToPrint
                        else:
                            rowOfFrames = np.concatenate((rowOfFrames, frameToPrint), axis = 1)
                            #image_row = np.concatenate((image_row, resized_frame), axis = 1)
                        j+=1
                    # After row of images has been created. Append it to the Image Matrix
                    if (i == 0):
                        imageMatrix = rowOfFrames
                    else:
                        imageMatrix = np.concatenate((imageMatrix, rowOfFrames), axis = 0)
                    i+=1

                # Print and return the resulting Image Matrix
                # cv.imshow("Image Matrix", imageMatrix)
                # Create the next ImageMatrix object
                imageMatrix = ImageMatrix(imageMatrix, self.__timestampQueue)
                # Wait for keyboard input
                # cv.waitKey(5)

                # Increment frame index for processing of next image matrix
                self.setFrameIndex(self.getFrameIndex() + 1)
                return imageMatrix

# if __name__ == "__main__":
    # Create ImageProcessor
    # imageProcessor = ImageProcessor()
 
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

#     cap = cv.VideoCapture('Model3Labeled1.mp4')
 
 
# #check if the video capture is open
# if(cap.isOpened() == False):
#     print("Error Opening Video Stream Or File")
 
 
# while(cap.isOpened()):
#     ret, frame =cap.read()
 
#     if ret == True:
#         cv.imshow('frame', frame)
 
#         if cv.waitKey(0)  == ord('q'):
#             break
 
#     else:
#         break
 
 
# cap.release()
# cv.destroyAllWindows()



                    


        



