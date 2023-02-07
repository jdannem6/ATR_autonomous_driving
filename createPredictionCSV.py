# This file is used to create CSV files that contain the control data 
# predictions between multiple models and the actual human input
# Written by Justin Dannemiller 

from cgi import print_directory
from json import detect_encoding
import os
import csv
import natsort
import glob

modelDirectoryPaths = [] # list of the directory paths of the models to be
                         # compared. Each directory stores the predictions 
                         # of a model on the same input matrices
modelDirectoryNames = [] 

detectionPath = os.getcwd() + '/Detection_Data'

# Retrieve the names of all model directories
for directoryName in os.listdir(detectionPath):
    directoryPath = detectionPath + '/' + directoryName
    if os.path.isdir(directoryPath):
        modelDirectoryNames.append(directoryName)
        modelDirectoryPaths.append(directoryPath)

controlDataPredictionList = [] # List containing, for each model, the set of 
                               # predictions made on the input matrices
confidenceLevelsList = [] # List containing, for each model, the set of 
                          # confidence levels corresponding to the predictions
# Retrieve and add the sets of predictions and CL for each model
for directoryPath in modelDirectoryPaths:
    controlDataPredictions = [] # set of predictions made by given model
    predictionConfidenceLevels = [] # corresponding confidence levels
    # Get all predictions made by the model
    baseLabelFileName = 'Model1_RawMatrices1_' # base for file names
    # Indices for index based loop
    startingIndex = 1
    finalIndex = 2939
    currentIndex=startingIndex
    # Default values for prediction and confidence level
    controlPrediction = 0.0

    while (currentIndex <=finalIndex):
        fileName = baseLabelFileName + str(currentIndex) + ".txt"
        filePath = directoryPath + '/labels/' + fileName
        # If the requested file exists, retrieve and store the prediction and associated 
        # confidence level from within it
        if os.path.isfile(filePath):
            with open(filePath, 'r') as predictionFile:
                # Take only first line in file, as we are only interested in one prediction
                firstLine = predictionFile.readline() 
                # Extract the integer label and confidence level corresponding to the prediction
                valuesInLabel = firstLine.split(' ')
                integerLabelOfPrediction = valuesInLabel[0]
                predictionConfidence = valuesInLabel[-1]
                # Calculate the corresponding rotation amount of the prediction
                lowerBoundRotation = -2.0
                intervalWidth = round(0.1, 1) # size of interval for control data
                # integer label 0 corresponds to the lower bound of rotation data,
                # and each label is separated by intervalWidth of rotationData
                controlPrediction = round(lowerBoundRotation + int(integerLabelOfPrediction)*intervalWidth, 1)
            # Otherwise, if the file does not exist (no prediction made for given image), 
            # use the previous control prediction and confidence level
        controlDataPredictions.append(controlPrediction)
        predictionConfidenceLevels.append(predictionConfidence)
        currentIndex +=1
    # # Before traversing to next model, add the set of prediction data to the lists
    controlDataPredictionList.append(controlDataPredictions)
    confidenceLevelsList.append(predictionConfidenceLevels)

    # for predictionFileName in natsort.natsorted(glob.glob(directoryPath + '/labels/*.txt')):
    #     with open(predictionFileName, 'r') as predictionFile:
    #         # Take only first line in file, as we are only interested in one prediction
    #         firstLine = predictionFile.readline() 
    #         # Extract the integer label and confidence level corresponding to the prediction
    #         valuesInLabel = firstLine.split(' ')
    #         integerLabelOfPrediction = valuesInLabel[0]
    #         predictionConfidence = valuesInLabel[-1]
    #         # Calculate the corresponding rotation amount of the prediction
    #         lowerBoundRotation = -2.0
    #         intervalWidth = round(0.1, 1) # size of interval for control data
    #         # integer label 0 corresponds to the lower bound of rotation data,
    #         # and each label is separated by intervalWidth of rotationData
    #         controlPrediction = round(lowerBoundRotation + int(integerLabelOfPrediction)*intervalWidth, 1)

    #         # Add the prediction data to the list
    #         controlDataPredictions.append(controlPrediction)
    #         predictionConfidenceLevels.append(predictionConfidence)

    # # Before traversing to next model, add the set of prediction data to the lists
    # controlDataPredictionList.append(controlDataPredictions)
    # confidenceLevelsList.append(predictionConfidenceLevels)

# Print the number of predictions for each model
i = 0
for model in controlDataPredictionList:
    print("Model " + str(i) + ": " + str(len(model)))
    i +=1
# Get the true actual input of the human user
""" I got rid of this section for now because I am currently using the raw data
    instead of the processed version of the human input. Uncomment and finish
    this later if you need the processed version"""
# pathToActualInput = os.getcwd() + '/Processed_Data/Model1_TestingSet/labels/'
# for inputFileName in natsort.natsorted(glob.glob(pathToActualInput + '*.txt')):
#     with open(inputFileName, 'r') as controlInputFile:
#         firstLine = controlInputFile.readline()

# for row in controlDataPredictionList[0]:
#     print(row)
# To the CSV file, add labels for each model
with open('controlDataComparison.csv', 'r') as inputFile, \
     open('controlDataComparison2.csv', 'w') as outputFile:
    CSVReader = csv.reader(inputFile)
    CSVWriter = csv.writer(outputFile)
    headerLine = CSVReader.__next__()
    # Add label for each model to be compared
    for directoryName in modelDirectoryNames:
        headerLine.append(directoryName)
    CSVWriter.writerow(headerLine)

    # Add all of the human control input and the corresponding model predictions
    i=0
    for controlInput in CSVReader:
        if controlInput is not None:
            for j in range(len(controlDataPredictionList)):
                # print("i: " +str(i))
                # print("j:" +str(j))
                controlInput.append(controlDataPredictionList[j][i])
            CSVWriter.writerow(controlInput)
            i += 1

