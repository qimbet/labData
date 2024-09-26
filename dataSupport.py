#!/usr/bin/env python3

#Data entry support for the Vertebrate lab at UBC. 
#This is framework to facilitate data entry, and offer a platform off of which future data pipelines can be built.

#Jacob Mattie, August 21, 2024
#For questions, contact: jacob@qimbet.com

import os
import datetime as dt
import pandas as pd

DEBUG = False

programDirectory = os.path.dirname(os.path.realpath(__file__))  
dataDirectory = os.path.join(programDirectory, "Data")
if not os.path.exists(dataDirectory):
    os.makedirs(dataDirectory)  
    os.chdir(dataDirectory) 

#---------------------------------------------------------------------------------------------------------------
#
#                               FUNCTION DEFINITIONS
#
#---------------------------------------------------------------------------------------------------------------

def d(input):
    if(DEBUG == True):
        print(input)

def newTestSeries():    #Sets up a new directory for a test series. Creates a table through newTable(dataList). Returns a directory
    os.chdir(dataDirectory)
    seriesName = input("Setting up a new test series. What species is being studied? ")
    seriesName = seriesName.title()
    seriesDataRepo = seriesName + " Data Repository"

    seriesPath = os.path.join(os.getcwd(), seriesDataRepo)
    if not os.path.exists(seriesPath):
        os.makedirs(seriesPath)  
    os.chdir(seriesPath)  

    dataList = []
    print(f"Setting up the data formats for {seriesName}. \nPlease enter the names of each data type that you're collecting (e.g. 'body length', 'weight', etc.)\n")
    newData = input("Enter a name for a data category and press enter: ")
    newData = newData.title()

    # if (len(dataList) == 0):
    #     dataList.append(newData)

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
    if userChoice.lower() == "edit":
        print("What would you like to edit?\n")
        choices = ["Remove data type", "Edit existing data type"]
        printChoose(choices) #Begin indexing at 1 for non-tech user intuitivity
        if editChoice == 1:
            print("Removing datatype: \nWhich datatype would you like to remove?\n")
            dataListRemove = printChoose(dataList)
            del dataList[dataListRemove]
            print(f"\nData list updated.\n Current data list is:\n")
            printListTab(dataList)

        elif editChoice == 2:
            print("Editing datatype. Which datatype would you like to revise?\n")
            dataListEdit = printChoose(dataList)
            while(True):
                updatedValue = input("Enter your corrected datatype:\n")
                confirm = input(f"You entered: \'{updatedValue}\'. Press 'enter on a blank field to confirm, or enter your value again.")
                if confirm == "":
                    dataList[dataListEdit] = updatedValue
                    break

    dataFileName = newFileNameCheck(seriesName)
    newTable(dataList, dataFileName)
    return seriesPath
        
def continueTestSeries():   #Lists file directories, allows selection. Returns a directory.
    os.chdir(dataDirectory)
    print("Select which test series you'd like to continue. \nThe current test series are:\n\n")
    fileList = os.listdir()
    count = 1

    for fileName in fileList:   #outputs available selection options from among list: "fileList"
        delimiter = " Data Repository"
        part = fileName.split(delimiter, 1)[0]
        print(f"{count} - \t{part}")
        count += 1

    userChoice = input("Enter the number representing the test series that you'd like to continue:\n")

#### SUGGESTION: make this following bit an independent function; f("data format parameter") ? e.g. f("path to Break statement")

    while(True): #input-checking
        if(userChoice.isdigit() == True):
            selected = int(userChoice)

            if 1 <= selected <= len(fileList):
                testSeries = fileList[selected-1] #-1 since lists start at index = 0
                testSeriesPath = os.path.join(dataDirectory, testSeries)
                print(f"Selected file: {testSeries}")
                break
            else:
                userChoice = input(f"You entered {userChoice}. That's out of bounds! Please enter an appropriate integer value: \n")
        else:
            userChoice = input(f"You entered {userChoice}. That's not an integer! Please enter an appropriate integer value: \n")
    
    os.chdir(testSeriesPath)
    d("Chosen working directory is: " + testSeriesPath)
    return(testSeriesPath)

#### End SUGGESTION

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
            if (int(editChoice) > 0 & int(editChoice) <= numRange):
                return (int(editChoice) - 1)
            else:
                editChoice = input("Your entered value is out of range! Please try again. \n")
                continue
        else:
            editChoice = input("Your entered value is not an integer! Please try again. \n")
            continue

def listString(list):   #UI. Lists options in a list with an associated index. Pairs with userInputInteger(list)
    num = 1
    for element in list:
        print(f"{num} - {element}\n")
        num += 1
    return

def printChoose(inputList):
    listString(inputList)
    choice = userInputInteger(inputList) -1 
    return choice

def printListTab(dataList):
    for element in dataList:
        print(element, end ="\t")
    print("\n\n")
    
#---------------------------------------------------------------------------------------------------------------
#
#                               MAIN FUNCTION
#
#---------------------------------------------------------------------------------------------------------------

count = 1
choiceList = ["Set up a new test series", "Continue a test series"] ###################################################    STARTUP USER CHOICES

print("Welcome!\nWhat would you like to do? Enter a numeric value to select an option.\n\n")

for element in choiceList:
    print(f"{count} - \t{element}")
    count += 1
userChoice = input("\n")

programRunList = ["Start a new test series", "Continue an existing test series"]
printChoose(programRunList)

if runMode == 1:
    testDir = newTestSeries() #returns the directory of the new test series
elif runMode == 2:
    testDir = continueTestSeries()    #returns the directory of the test to be continued


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