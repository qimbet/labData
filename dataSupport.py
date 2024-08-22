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
    if(DEBUG = True):
        print(input)

def newTestSeries():    #Sets up a new directory for a test series. Creates a table through newTable(dataList). Returns a directory
    seriesName = input("Setting up a new test series. What species is being studied? ")
    seriesDataRepo = seriesName.title() + " Data Repository"

    seriesPath = os.path.join(os.getcwd(), seriesDataRepo)
    if not os.path.exists(seriesPath):
        os.makedirs(seriesPath)  
        os.chdir(seriesPath)  

    dataList = []
    print("Setting up the data formats. Please enter the names of each data type that you're collecting (e.g. 'body length', 'weight', etc.)\n")
    newData = input("Enter a name for a data category and press enter: ")
    while (True):
        userChoice = input(f"{newData.title()} added! Enter 'edit' if you'd like to edit this entry, or enter your next data type. \nWhen you're done entering data types, leave the input blank and press 'Enter'.\n\nNew datatype: ")
        if (userChoice.lower() == "edit"):
            newData = input("Please enter the corrected data type name: ")
            continue
        dataList.append(newData.title()) 
        newData = userChoice
        if (newData == ""):
            print("-")
            break

    print("Current data list is: \n")
    for element in dataList:
        print(element, end ="\t")
    print("\n\n")

    newTable(dataList)

    os.chdir(programDirectory)
    return seriesPath
        
def continueTestSeries():   #Greetings. Lists file directories, allows selection. Returns a directory.
    os.chdir(dataDirectory)
    print("Select which test series you'd like to continue. \nThe current test series are:\n\n")
    fileList = os.listdir()
    count = 1

    for fileName in fileList:
        delimiter = " Data Repository"
        part = fileName.split(delimiter, 1)[0]
        print(f"{count} - \t{part}")
        count += 1

    userChoice = input("Enter the number representing the test series that you'd like to continue:\n")

    while(True):
        if(userChoice.isdigit() == True):
            selected = int(userChoice)

            if 1 <= selected < len(fileList):
                testSeries = fileList[selected-1] #-1 since lists start at index = 0
                testSeriesPath = os.path.join(dataDirectory, testSeries)
                print(f"Selected file: {testSeries}")
                break
            else:
                userChoice = input(f"You entered {userChoice}. That's not a valid choice! Please enter an appropriate integer value: \n")
        else:
            userChoice = input(f"You entered {userChoice}. That's not a valid choice! Please enter an appropriate integer value: \n")
    
    os.chdir(testSeriesPath)
    d("Chosen working directory is: " + testSeriesPath)
    return(testSeriesPath)

def newFile(seriesName):    #sets up a new .txt file for a series, date-marked. Increments a counter if a file already exists for today
    now = dt.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    entryDate = f"{day}-{month}-{year}"

    newDataFileName = f"{entryDate} - {seriesName} data"

    if os.path.exists(newDataFileName + ".txt"):
        lastChar = newDataFileName[-1]
        if (lastChar.isdigit() == True):
            iteration = int(lastChar)+1
            newDataFileName[:-1] + str(iteration)
        else:
            newDataFileName = newDataFileName + " - 1"

def newTable(dataList):
    dataTable = pd.DataFrame(columns=dataList)



    return dataTable
#---------------------------------------------------------------------------------------------------------------
#
#                               MAIN FUNCTION
#
#---------------------------------------------------------------------------------------------------------------


choiceList = ["Set up a new test series", "Continue a test series"]

count = 1
print("Welcome!\nWhat would you like to do? Enter the numeric value to select an option.\n\n")

for element in choiceList:
    print(f"{count} - \t{element}")

userChoice = input("\n")
while(True):
    if (userChoice.isdigit() == True):
        choice = int(userChoice)
        if choice == 1:
            x = newTestSeries() #returns the directory of the new test series
            break
        elif choice == 2:
            continueTestSeries()    #returns the directory of the test to be continued
            break
    else:
        userChoice = input("That's not a valid choice. Please enter another value.\n")



dataTable = pd.DataFrame(columns=dataList)


with open(newDataFileName+".txt", "w") as file:
    file.write(dataTable.to_string(index=False))    

x= input("Press enter to end the program.\n")