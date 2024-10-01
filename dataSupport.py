#!/usr/bin/env python3

#Jacob Mattie, August 21, 2024
#j_mattie@live.ca

import os
import datetime as dt
import pandas as pd
import sqlite3 as sql

DEBUG = True

#---------------------------------------------------------------------------------------------------------------
#
#                               FUNCTION DEFINITIONS
#
#---------------------------------------------------------------------------------------------------------------

def d(inVal): #Debug
    if(DEBUG == True):
        if inVal == "":
            print("\n")
        else:
            print(inVal)

def newTestSeries():    #Sets up a new directory for a test series. Creates a table through newTable(dataList). Returns a directory
    os.chdir(dataDirectory)
    seriesName = input("Setting up a new test series. Enter the name of the species being studied: \n\n")
    seriesName = seriesName.title()
    seriesDataRepo = seriesName + " Data Repository"

    seriesPath = os.path.join(os.getcwd(), seriesDataRepo)
    if not os.path.exists(seriesPath):
        os.makedirs(seriesPath)  
    os.chdir(seriesPath)  

    dataList = []
    print(f"Setting up the data formats for: {seriesName}. \nPlease enter the names of each data type that you're collecting (e.g. 'body length', 'weight', etc.)\n")
    newData = input("Enter a name for a data category and press enter: ")
    newData = newData.title()

    while (True):
        userEntry = input(f"{newData} added! \nEnter 'edit' if you'd like to edit this entry, or enter your next data type. \nWhen you're done entering data types, leave the input blank and press 'Enter'.\n\nNew datatype: ")
        if (userEntry.lower() == "edit"):
            newData = input(f"Revising the entry: {newData.title()}.\nPlease enter the corrected data type name: ")
            print("\n")
            newData = newData.title()
        elif (userEntry == ""):
            dataList.append(newData) 
            print("\n\n")
            break
        else: 
            dataList.append(newData) 
            newData = userEntry.title()

    print("Current data list is: \n")
    printListTab(dataList)

    userChoice = input("Proceed? If you woud like to edit the list, enter 'edit'. Otherwise, press enter on a blank field to continue.\n")
    while(True):
        if userChoice.lower() == "edit":
            print("What would you like to edit?\n")
            print("Current data types are: \n")
            printListTab(dataList)
            print("You may enter a task-associated numerical value, or press enter on a blank field to continue.\n")
            choices = ["Remove data type", "Edit existing data type", "Add data type"]
            editChoice = printChoose(choices)
            
            if editChoice == 0:
                print("Removing datatype: \nWhich datatype would you like to remove?\n")
                dataListRemove = printChoose(dataList)
                del dataList[dataListRemove]
                print(f"\nData list updated.\n Current data list is:\n")
                printListTab(dataList)

            elif editChoice == 1:
                print("Editing datatype. Which datatype would you like to revise?\n")
                dataListEdit = printChoose(dataList)
                updatedValue = input("Enter your corrected datatype:\n")
                dataList[dataListEdit] = updatedValue.title()
                    
            elif editChoice == 2:
                newValue = input("What parameters would you like to add?\n")
                newValue = newValue.title()
                print(f"{newValue} added!")
                dataList.append(newValue)

            elif editChoice == "":
                break              
        elif userChoice == "":
            break
        else: 
            userChoice = input("You did not enter a valid value!\n Press 'enter' on a blank field to continue to data input, or enter 'edit' to modify the test series parameters.\n")

    return seriesPath
        
def selectTestSeries():   #Lists file directories, allows selection. Returns a directory.
    os.chdir(dataDirectory)
    print("Select which test series you'd like to continue. \nThe current test series are:\n\n")
    fileList = os.listdir()

    d("\n\nfile list: ")
    d(fileList)

    directoryOptions = []
    for fileName in fileList:   #outputs available selection options from among list: "fileList"
        delimiter = " Data Repository"
        part = fileName.split(delimiter, 1)[0]
        directoryOptions.append(part)
        

    d("printchoose fileList: \n\n")
    userChoice = printChoose(directoryOptions)
    testSeries = fileList[userChoice]
    testSeriesPath = os.path.join(dataDirectory, testSeries)
    print(f"Opened test series: {directoryOptions[userChoice]}")
    # os.chdir(testSeriesPath)
    d("Working directory is: " + testSeriesPath)
    return(testSeriesPath)

def newFileNameCheck(seriesName):    #returns a new .txt filename for a series, date-marked. Increments a counter if a file already exists for today
    now = dt.datetime.now()
    day = now.day
    month = now.strftime("%B")
    year = now.year
    entryDate = f"{day} {month}-{year}"

    newDataFileName = f"{entryDate} - {seriesName} data"

    if os.path.exists(newDataFileName + ".txt"):
        lastChar = newDataFileName[-1]
        if (lastChar.isdigit() == True):
            iteration = int(lastChar)+1
            newDataFileName[:-1] + str(iteration)
        else:
            newDataFileName = newDataFileName + " - 1"
    
    return(newDataFileName+".txt")

def newTable(dataList, newDataFileName):     #Initializes a text file with a first line of \t delimited column names, given by dataLists. Returns(?) a pd.Dataframe object
    dataTable = pd.DataFrame(columns=dataList)


    #This is where I need to fix. It opens its own writing file: this should not be its responsibility
    with open(newDataFileName+".txt", "w") as file:
        # file.write(dataTable.to_string(index=False))
        for element in dataList:
            file.write(f"{element} \t")
    return dataTable

def userInputInteger(inputList): #Prompts the user for an integer input within an allowable range (len(inputList)). UI. Returns index of selected list item, starting at 0
    numRange = len(inputList)
    editChoice = input("Enter the numeric value corresponding to your selection: ")
    while(True):
        if(editChoice.isdigit() == True):
            editChoice = int(editChoice)
            if (editChoice > 0 & editChoice <= numRange):
                return (editChoice - 1)
            else:
                editChoice = input("Your entered value is out of range! Please try again. \n")
                continue
        elif (editChoice == ""):
            return ""
        else:
            editChoice = input("Your entered value is not an integer! Please try again. \n")
            continue

def listString(list):   #UI. Lists options in a list with an associated index. Pairs with userInputInteger(list)
    num = 1
    for element in list:
        print(f"{num} - {element}")
        num += 1
    print("\n")
    return

def printChoose(inputList):
    listString(inputList)
    choice = userInputInteger(inputList)
    return choice

def printListTab(dataList):
    for element in dataList:
        print(element, end ="\t")
    print("\n\n")

def enterData():   
    print("test line")
#---------------------------------------------------------------------------------------------------------------
#
#                               MAIN FUNCTION
#
#---------------------------------------------------------------------------------------------------------------

if True: #Directory setup
    programDirectory = os.path.dirname(os.path.realpath(__file__))  
    directoryList = ["Data", "Graphs"]

    directoryPathList = []
    for element in directoryList:
        dir = directoryPathList.append(os.path.join(programDirectory, element))
        if not os.path.exists(dir):
            print(f"\nNo {element} directory found!\n...\nSetting up {element} directory in {programDirectory}\n\n")
            os.makedirs(dir)  
    
    dataDirectory = directoryPathList[0]
    graphsDirectory = directoryPathList[1]

os.chdir(dataDirectory) 

programRunList = ["Start a new test series", "Continue an existing test series", "Export full data series", "Analyze Data"]
exportOptions = ["Export SQL Database", "Export .csv", "Export .pdf"]
analyzeOptions = ["Graph data", "Statistical trends"]



print("Data support code written by Jacob Mattie, 2024\njacob@qimbet.com\ngithub.com/qimbet\nWelcome!\nI'm thrilled to help you out with your data management!\nWhat would you like to do? Enter a numeric value to select an option.\n\n")

runMode = printChoose(programRunList)

if runMode == 0:    #programRumList entry index
    testDir = newTestSeries() #returns seriesPath
    
    seriesName = os.path.split(testDir)

    delimiter = " Data Repository"
    seriesName = seriesName[1].split(delimiter, 1)[0]  #returns, e.g. "Horse" from "Horse Data Repository"        


    # dataFileName = newFileNameCheck(seriesName)
    # newTable(dataList, dataFileName)
elif runMode == 1:
    testDir = selectTestSeries()    #returns the directory of the test to be continued
    d("running established test series as selected")
elif runMode == 2:
    print("not yet")
elif runMode == 3: 
    print("not yet")
    
os.chdir(testDir)


# dataTable = pd.DataFrame(columns=dataList)
activeTestSeries = os.path.basename(os.getcwd())
activeFileName = newFileNameCheck(activeTestSeries)

with open(activeFileName, "w") as file:
    while(True):
        data = input("PROGRAM: you can enter data here: ")
        file.write(data + "\n")  
        print("data added.\n")
        if data == "":
            break

x= input("Press enter to end the program.\n")