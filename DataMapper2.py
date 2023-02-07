# Data Mapper
# Part of the Autonomous Driving Project
# Written by Justin Dannemiller
# Last Edited 6/29/22

# This file defines the methods and attributes of the imageProcessor class, 
# the class used to create NxM image matrices from a video stream

from concurrent.futures import process
from Data_Processors.ControlProcessor import ControlProcessor
from Data_Processors.imageProcessor import ImageProcessor
import cv2 as cv
import os
from threading import Thread # Needed for multithreading
import math # needed for floor function
import shutil # needed for deleting directories
import csv

if __name__ == "__main__":
    ## Create an imageProcessor and controlProcessor objects to process the raw
    ## data
    imageProcessor = ImageProcessor()
    controlProcessor = ControlProcessor()

    ## Configure the directories for both processors
    mainDirectory = os.getcwd()
    """ Consider generalizing this later on by having the user input
        the names of the folders or the paths storing the images and 
        control segments """
    # Create names of control and image directories
    rawDataStorage = mainDirectory + '/Raw_Data'
    rawImageDirectory = rawDataStorage + '/Model0_Lesson4/ImageStorage'
    rawControlDirectory = rawDataStorage + '/Model0_Lesson4/ControlStorage'
    # Set processors' directories
    imageProcessor.setImageDirectory(rawImageDirectory)
    controlProcessor.setControlDirectory(rawControlDirectory)

    # Read control data segments into memoryS
    controlProcessor.readRawControlData()

    # # Create new, empty directory for storage of image matrices
    # matrixDirectory = r'/home/jdannem6/opencv/Gamepad/MatrixStorage'
    # shutil.rmtree(matrixDirectory) # delete previous contents
    # os.mkdir(matrixDirectory) # replace with empty directory

    # # # Create new, empty directory for storage of control data 
    # controlDirectory = r'/home/jdannem6/opencv/Gamepad/ProcessedControlData'
    # shutil.rmtree(controlDirectory) # Delete previous directory
    # os.mkdir(controlDirectory)

    # Begin producing Data Matrices
    # Request next image matrix from Image Processor
    nextMatrixObject = 0
    fileIndex = 0

    # A list of all the raw control data points corresponding to the
    # control data segments that selected in the processed data
    listofSelectedRawInput = []

    nextIndex = 0 # Index of next frame to include in matrix
    while (nextMatrixObject is not None):
        nextMatrixObject = imageProcessor.nextImageMatrix2()
        if nextMatrixObject is not None:
            # Extract timestamp information
            timestamps = nextMatrixObject.getTimestamps()
            # Extract the image matrix from the object 
            nextMatrix = nextMatrixObject.getImageMatrix()

            # Request control data segement around each timestamp
            namingTimestamp = -1
            windowSize = 3
            ## On suggestion of Dr.Kim, we will only get the control data
            # pertaining to the last frame in the image matrix, so the following
            # commented code is unneceesary now, but kept for later use
            controlDataBlock = [] # Stores the control data for entire image matrix
            # for timestamp in timestamps:
            #     # Ignore all timestamps flagged with -1 value)
            #     if (timestamp is not -1):
            #         # The first nonnegative timestamp is used to name the files
            #         if (namingTimestamp == -1):
            #             namingTimestamp = timestamp

            #         # Define lowerBound and upper bound of time interval for control
            #         # data
            #         lowerBound = timestamp - int(windowSize/2)
            #         upperBound = timestamp + windowSize/2
            #         # Define corresponding time interval
            #         timeInterval = [lowerBound, upperBound]
            #         # Request control data occurring within timeInterval
            #         controlDataSegments = controlProcessor.getDataInInterval(timeInterval)
            #         # Accumulate control data segements
            #         for segment in controlDataSegments:
            #             controlDataBlock.append(segment)

            #         # If requested time interval is valid, extract the associated control
            #         # data for later storage
            #         if (controlDataBlock is not None):


            #             # Extract the control data from the controlBlock
            #             fileData = "" # control data stored in txt file
            #             segmentIndex = 0 
            #             while (segmentIndex < len(controlDataBlock)):
            #                 dataSegment = controlDataBlock[segmentIndex]
            #                 # Store the axis data in the txt file
            #                 axisData = dataSegment['axesValues']
            #                 print("Instantaneous axis data:" +str(axisData))
            #                 fileData +=  axisData +"\n"
            #                 segmentIndex += 1


            # Request control data segment for the last added frame in the 
            # image matrix
            timestamp = timestamps[-1] # get timestamp of last added frame
            # Ignore all timestamps flagged with -1 value)
            if (timestamp != -1):
                # The first nonnegative timestamp is used to name the files
                if (namingTimestamp == -1):
                    namingTimestamp = timestamp

                # Define lowerBound and upper bound of time interval for control
                # data
                lowerBound = timestamp - int(windowSize/2)
                upperBound = timestamp + windowSize/2
                # Define corresponding time interval
                timeInterval = [lowerBound, upperBound]
                # Request control data occurring within timeInterval
                #controlDataBlock = controlProcessor.getDataInInterval(timeInterval)
                
                # # Calculate the time in milliseconds between frames
                # playbackRate = imageProcessor.getPlaybackRate()
                # timeBetweenFrames = int(1000 * 1/playbackRate)
                # controlDataSegment = controlProcessor.getNearestDataSegment(
                #     timestamp, timeBetweenFrames)

                # Get the control data segment occurring immediately after the timestamp
                controlDataSegment = controlProcessor.getNearestDataSegment2(timestamp)

                # if valid controlDataSegment is retrieved, create a label for the image
                # containing the control data segment, the coordinates of the center
                # of the matrix (expressed as a ratio from 0 to 1) and the width
                # and height of the image matrix (both expressed as ratios from 0 to 1)
                if (controlDataSegment is not None):
                    fileData = controlDataSegment['Rotation']
                    # As of now, the entire image matrix is being selected, so 
                    # the center, width, and height are fixed
                    x_center = "0.5"
                    y_center = "0.5"
                    width = "1"
                    height = "1"
                    # Append the image dimension information to fileData
                    fileData += " " + x_center
                    fileData += " " + y_center
                    fileData += " " + width
                    fileData += " " + height

                    # Extract and save the corresponding raw control data for 
                    # comparison to model predictions
                    rawData = controlDataSegment['Raw_Control']
                    listofSelectedRawInput.append(rawData)

                else:
                    fileData = ""

                # If requested time interval is valid, extract the associated control
                # data for later storage
                #if (controlDataBlock is not None):

                    # print("Control Data Block:" + str(controlDataBlock))
                    # Extract the control data from the controlBlock
                    # fileData = "" # control data stored in txt file
                    # segmentIndex = 0 
                    # while (segmentIndex < len(controlDataBlock)):
                    #     dataSegment = controlDataBlock[segmentIndex]

                    #     # Store the axis data in the txt file
                    #     axisData = dataSegment['axesValues']
                    #     fileData +=  axisData +"\n"
                    #     segmentIndex += 1

            ## Store the control data in a txt file
            # Change to ProcessedControlData directory 
            processedDataDirectory = mainDirectory + '/Processed_Data/Model1_TestingSetDupe'
            controlDirectory = processedDataDirectory  + '/labels'
            #controlDirectory = r'/home/jdannem6/opencv/Gamepad/ProcessedControlData'
            os.chdir(controlDirectory)
            # Create the name of the file to store the control data within
            controlFilename = "Matrix" + str(fileIndex) + ".txt"

            # Write the control data to file if a valid control data segment 
            # was retrieved
            if (controlDataSegment is not None):
                with open(controlFilename, "w") as textFile:
                    textFile.write(fileData)

            ## Store the corresponding iamge matrix in a jpg file
            # Change to the MatrixStorage directory
            matrixDirectory = processedDataDirectory + '/images'
            os.chdir(matrixDirectory)
            # Create name for matrix file
            matrixFileName = "Matrix" + str(fileIndex) + ".jpg"
            # Write matrix to file if there is a valid control
            # data segment for it
            if (controlDataSegment is not None):
                cv.imwrite(matrixFileName, nextMatrix)
                # Increment file index for next set of control data - image matrices
                fileIndex += 1



            # # Naming convention for control files: "Model" + Model_ID + 
            # # "Control" + first timestamp not equal to -1
            # # Create the name of the file to store the control data within
            # controlFilename= "Model0Control" + str(namingTimestamp) + ".txt"
            # # Write control data to file
            # # Change to ProcessedControlData folder
            # os.chdir(controlDirectory)
            # with open (controlFilename, "w") as textFile:
            #     textFile.write(fileData)

            # # Naming convention for image matrix files: "Model" + Model_ID + 
            # # "Matrix" + first first timestamp not equal to -1
            # imageFileName = "Model0Matrix" + str(namingTimestamp) + ".jpg"
            # # Write image data to file
            # os.chdir(matrixDirectory) # Change to matrix directory
            # cv.imwrite(imageFileName, nextMatrix)
    
    # Create dataset yaml file used in the model training process to label
    # images with the correct class/label
    """ Make this function more generalized later by replacing the hard-coded
        values with the use of Control processor functions that retrieve the
        desired parameters"""
    lowerBoundControl = -2.0
    upperBoundControl = 2.0
    intervalSize = round(0.1, 1)

    # Create strings to describe the train and test paths for model
    trainPath = 'train: ../OpenCR_Model0Processed/images/\n'
    testPath = 'val: ../OpenCR_Model0Processed/images/\n\n\n'

    
    # Create string for the number of classes
    classesComment = '# number of classes\n'
    classNumberString = 'nc: ' + str(controlProcessor.getNumberOfClasses()) +"\n\n\n"

    # Create a string listing all class names
    classListString = 'names: ['
    currentInterval = lowerBoundControl
    while (currentInterval <= upperBoundControl):
        currentClassName = str(currentInterval)
        classListString += '"' + currentClassName + '",'
        currentInterval = round(currentInterval + intervalSize, 1)
    classListString += ']\n'

    # Write all the strings to a yaml file
    os.chdir(processedDataDirectory)
    datasetFile = open("dataset.yaml", "w")
    datasetFile.write(trainPath)
    datasetFile.write(testPath)
    datasetFile.write(classesComment)
    datasetFile.write(classNumberString)
    datasetFile.write(classListString)
    datasetFile.close()

    os.chdir(mainDirectory)
    # Write all the selected raw control data points to a CSV file
    with open('controlDataComparison.csv', 'w') as controlCSV:
        CSVWriter = csv.writer(controlCSV)
        # Write caption to csv for the input data
        CSVWriter.writerow(["Human input rotation"])
        # Write all of the raw data segments
        for controlInput in listofSelectedRawInput:
            CSVWriter.writerow([controlInput])



