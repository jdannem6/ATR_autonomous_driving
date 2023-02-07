# Control Processing Program
# Part of the Autonomous Driving Project
# Written by Justin Dannemiller
# Last Edited 6/9/22

import os
import time # Needed for timestamps
import json
import math


# I think Dr. Kims of segmenting raw data and giving it some kind of name
# that includes the timestamp is going to be very beneficial. One of
# the reason for this is that with one file storing all the raw control data, 
# there will likely be one thread writing to the file while another is reading
# from it, and this could potentially causes issues.

# Class which reads control data from a controller, processes it, and stores
# the processed data for later access
class ControlProcessor:
    def __init__(self, pollInterval = 0.05):
        # Set the initialization timestamp
        self.__pollInterval = pollInterval
        self.__firstTimestamp = time.time()
        self.__controlDataSegments = []
        self.__controlDirectory = ""
        self.__numberOfClasses = 0

    # Sets the control directory from which the processor will read raw
    # control data segmetns
    def setControlDirectory(self, controlDirectory):
        self.__controlDirectory = controlDirectory

    # Returns the index of the element that has the lowest timestamp that lies
    # in the range of the time given time interval
    def __getLowerIndex(self, lowerBound):
        # Initialize the low and high indices with which to conduct the search
        low = 0
        high = len(self.__controlDataSegments)
        # Perform binarySearch of segments until the element with lowest timestamp
        # greater than lowerBound is found
        while True:
            # Calculate the index of element in middle of search range
            middleIndex = int(math.floor((low + high)/2))
            middleTimestamp = self.__controlDataSegments[middleIndex]['timestamp']
            # If the middle timestamp is not bounded below by lowerBound, perform next 
            # '
            #search on the upper half of the search range
            if (middleTimestamp < lowerBound):
                low = middleIndex
                high = high
            # Otherwise, if the middle timestamp falls within the time interval
            elif (middleTimestamp > lowerBound):
                # If the previous timestmap is greater than the lowerBound, then
                # Current element corresponds to the lower bounding index
                if (self.__controlDataSegments[middleIndex - 1]['timestamp'] < lowerBound):
                    return middleIndex
                # Otherwise, we haven't found lower bounding index yet; conduct
                # next search on lower half of range
                else:
                    low = low
                    high = middleIndex
            # Else if middleTimestamp is same as lowerBound, middleIndex is lower
            # bounding index
            else:
                return middleIndex

    # Returns the index of the element that has the highest timestamp lying within the
    # given time interval
    def __getUpperIndex(self, upperBound):
        # Initalize the low and high idneices with which to conduct the search
        low = 0
        high = len(self.__controlDataSegments)
        # Perform binary search of segments until element with highest timestamp
        # below upperBound is found
        while True:
            # Calculate the index of the middle element within search range
            middleIndex = int(math.floor((low + high)/2))
            middleTimestamp = self.__controlDataSegments[middleIndex]['timestamp']
            # If the middle timestamp is not bounded above by the upperBound,
            # perform next search on lower half of search range
            if (middleTimestamp > upperBound):
                low = low
                high = middleIndex
            # Otherwise if middle timestamp is bounded above by upperBound
            elif (middleTimestamp < upperBound):
                # and if the next element is greater than the upperBound, then 
                # the upperIndex has been found
                if (self.__controlDataSegments[middleIndex + 1]['timestamp'] > upperBound):
                    return middleIndex
                # otherwise, perform the next search on the upper half of the 
                # search range
                else:
                    low = middleIndex
                    high = high
            # Otherwise, the middleIndex is the upperIndex
            else:
                return middleIndex

    # Takes a time interval and returns all processed control data segemtns 
    # occurring within that time interval 
    def getDataInInterval(self, timeInterval):
        # Perform error checking on jsonObject
        lowerBound = timeInterval[0]
        upperBound = timeInterval[1]
        # Return error if lower bound not less than upper bound
        if lowerBound >= upperBound:
            return "Error: Lower bound must be greater than upper bound"
        # Return error if either bound in timeInterval lie outside the range of 
        # timestamps in controlDataSegments
        firstTimestamp = self.__controlDataSegments[0]['timestamp']
        lastTimestamp = self.__controlDataSegments[-1]['timestamp']
        if (lowerBound < firstTimestamp or upperBound > lastTimestamp):
            print("Error: control data not available in requested time interval")
            print("lowerBound: " + str(lowerBound) + " firstTimestamp: " + str(firstTimestamp))
            print("upperBound: " + str(upperBound) + " lastTimestamp: " + str(lastTimestamp))
            return None 
        else:
            lowerIndex = self.__getLowerIndex(lowerBound)
            upperIndex = self.__getUpperIndex(upperBound)
            # Insert all data segments whose timestamps fall within the
            # timeInteval into desiredData list
            desiredData = []
            i = lowerIndex
            while (i <= upperIndex):
                desiredData.append(self.__controlDataSegments[i]) # Add ith data segment to list
                i+=1
            return desiredData
        
    # Retrieves the first control data segement occurring after the given timestamp
    def getNearestDataSegment(self, timestamp, timeBetweenFrames):
        desiredIndex = int(math.ceil(timestamp/timeBetweenFrames))
        # Check if there exists control data corresponding to the desired index
        if (desiredIndex >= len(self.__controlDataSegments)):
            return None
        # Otherwise, there exists such a control data segment
        else:
            return self.__controlDataSegments[desiredIndex]

    # Retrieves the first control data segement occurring after the given timestamp
    # This version of the method is used in the case that the raw images being 
    # processed were not from a video capture, but from a directory. In such a
    # case there may not be a consistent amount of time between frames, so 
    # we can't simply index the frmaes
    def getNearestDataSegment2(self, timestampOfFrame):
        # Get first Data segment whose timestamp is greater
        # than timestampOfFrame
        nextSegments =[] 
        # Create list of all segments exceeding the desired timeframe
        for segment in self.__controlDataSegments:
            if segment['timestamp'] > timestampOfFrame:
                nextSegments.append(segment)
        # Return the first timestamp in the list
        nearestSegment = nextSegments[0]
        return nearestSegment

    # Sets the number of classes to segment the control data into
    # This function is used by the readRawControlData function
    def __setNumberOfClasses(self, desiredClassCount):
        """ Perform greater type checking later on"""
        self.__numberOfClasses = desiredClassCount

    # Reads raw control data segments from a folder and stores them in a data
    # structure for later processing
    # Takes as input the controlProcessor itself (implict) 
    def readRawControlData(self):
        ## Get list of all txt files storing control data segments
        controlFiles = []
        previousDirectory = os.getcwd()
        os.chdir(self.__controlDirectory)
        for filePath in os.listdir():
            # If file has .txt extension, add it to the list of control files
            if filePath.endswith(".txt"):
                controlFiles.append(filePath)
        ## Sort the control files such that they are arranged in order of
        ## timestamp
        controlFiles.sort()

        ## Process each control data file
        """ For now, the rotation around the z-axis will be the only control data
            that is stored. This was decided as the rotational data is really the
            only control attribute that is related to where the turtlebot was 
            positioned relative to the black line. Note that how the values
            of this axis are processed depends on the range of potential values that
            can be observed on that axis. During the first test, the maximum value was
            0.8, so the following if statements reflect that. """
        for filePath in controlFiles:
            # Read the file's data
            with open(filePath, 'r') as filePtr:
                controlData = filePtr.read()
            # Extract rotational data
            rotationalData = controlData.split("angular:")[-1]
            zRotationData = rotationalData.split("z: ")[-1]

            # Convert rotational data to float
            # print(filePath)
            # print(zRotationData + "\n")
            zRotationData = float(zRotationData)

            ## Map a unique integer label to each control data segment
            intervalWidth = 0.10 # size of interval for control data
            rangeOfValues = 4.0
            # Calculate the total number of labels for the control data 
            # Needed for model training (plus 1 for 0.0)
            numberOfClasses = rangeOfValues/intervalWidth + 1 
            self.__setNumberOfClasses(numberOfClasses)
            integerLabel = int(zRotationData/intervalWidth)
            # Map Label to domain from 0 to numberOfLabels - 1
            integerLabel += int(self.getNumberOfClasses()/2)

            # Map
            # # Categorize the the rotational data into discrete levels for
            # # model training purposes
            # if (zRotationData == -2.0):
            #     rotationalData = "0"
            # elif (zRotationData > -2.0 and zRotationData <= -1.5):
            #     rotationalData = "1"
            # elif (zRotationData > -1.5 and zRotationData <= -1.0):
            #     rotationalData = "2"
            # elif (zRotationData > -1.0 and zRotationData <= -0.5):
            #     rotationalData = "3"
            # elif (zRotationData > -0.5 and zRotationData <= 0.0):
            #     rotationalData = "4"
            # elif (zRotationData > 0.0 and zRotationData <= 0.5):
            #     rotationalData = "5"
            # elif (zRotationData > 0.5 and zRotationData <= 1.0):
            #     rotationalData  = "6"
            # elif (zRotationData > 1.0 and zRotationData <= 1.5):
            #     rotationalData  = "7"
            # elif (zRotationData > 1.5 and zRotationData < 2.0):
            #     rotationalData  = "8"
            # else:
            #     rotationalData = "9"

            ## Extract the control segment's timestamp from its filename
            fileName = filePath.split('/')[-1]
            # Timestamp is listed before .txt file extension
            timestamp = fileName.split(".txt")[0]
            # Convert timestamp to float
            timestamp = float(timestamp)

            
            ## Create Control Data Segment storing the rotational Data and
            ## the corresponding timestamp
            controlSegment= {
                "timestamp" : timestamp,
                "Rotation" : str(integerLabel),
                "Raw_Control": zRotationData
            }

            # Apend the control data segment to the list
            self.__controlDataSegments.append(controlSegment)

        # Serialize json
        json_control = json.dumps(self.__controlDataSegments, indent = 4)
        ## Write to json file
        # Change back to previous directory
        os.chdir(previousDirectory)
        with open("RawControlData2.json", "w") as outputFile:
            outputFile.write(json_control)

    # Returns the total number of classes that the control data is segmented into
    # Used to write the dataset yaml file used in the model training process
    def getNumberOfClasses(self):
        return self.__numberOfClasses
