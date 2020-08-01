import random
from datetime import datetime, timedelta
import tkinter as tk

def RNG(numOfPeople, numOfDays, listOfNames):
    numOfPeople = int(numOfPeople)
    numOfDays = int(numOfDays)
    # empty list of RNG
    randomized = []
    # our cumalitive number of times someone was assigned
    totalOrder = {}
    # history of random assignments
    history = []
    # our iterator variable
    iteration = 1
    # filling up the list with the given argument
    for i in range(1, numOfPeople + 1):
        totalList = []
        randomized.append(i)
        for j in range(1, numOfPeople + 1):
            totalList.append({j: 0})
        totalOrder.update({i: totalList})
    # looping through the number of days given
    while (iteration <= numOfDays):
        while (True):
            # reset the order every time we have to randomized
            order = {}
            # shuffling the list
            random.shuffle(randomized)
            for (i, j) in zip(range(1, numOfPeople + 1), randomized):
                order.update({i: j})
            # increment each order in the totalOrder
            for ord in order.keys():
                rank = ord
                whoWasIt = order[ord]
                updateFinal(totalOrder, rank, whoWasIt)
            if (isValid(totalOrder,numOfPeople,numOfDays) == True):
                # apppend the random assingment to the history of assignments
                history.append(order)
                break
            else:
                #bad set of random numbers, so we backtrack
                for ord in order.keys():
                    rank = ord
                    whoWasIt = order[ord]
                    revertChanges(totalOrder,rank,whoWasIt)
        # increment the day
        iteration += 1
    #write to csv
    createCSVWithNames(numOfPeople)
    fillUpNames(history,listOfNames,numOfDays)


def isValid(dict, numOfPeople, numOfDays):
    number = numOfDays / numOfPeople
    flag = True
    for i in dict.keys():
        lst = dict[i]
        for j in lst:
            for k in j.keys():
                if j[k] > number:
                    flag = False
    return flag


def updateFinal(dict, rank, who):
    # get the value of the specified key
    lst = dict[rank]

    # update the value of the value of list
    for i in lst:
        for j in i.keys():
            if j == who:
                i[j] += 1
    dict.update({rank: lst})


def revertChanges(dict, rank, who):
    # get the value of the specified key
    lst = dict[rank]

    # update the value of the value of list
    for i in lst:
        for j in i.keys():
            if j == who:
                i[j] -= 1
    dict.update({rank: lst})


def createCSVWithNames(numPeople):
    #creating the file
    file = open("Rotation.csv",'w')
    #first field is days
    file.write("Date, ")
    #next fields are the ranks
    for i in range(1,numPeople+1):
        if i == numPeople:
            file.write(str(i))
        else:
            file.write(str(i) + ", ")
    #print new line
    file.write("\n")

def fillUpNames(listOfDict, namesList, numOfDays):
    #get the current date of this program execution
    currDate = datetime.date(datetime.now())
    #our counter
    day = 1
    #reopen the file that we want to append to
    file = open("Rotation.csv",'a')
    #length of the list of names
    lenOfList = len(namesList)

    while (day <= numOfDays):
        #write down the current date
        file.write(str(currDate) + ", ")
        #our counter
        counter = 1
        index = listOfDict[day - 1]
        for i in index.keys():
            #get the index of the name
            value = index[i]
            #get the name from the list
            name = namesList[value - 1]
            #if we are at the end, dont add ,
            if counter == lenOfList:
                file.write(name + "\n")
            else:
                file.write(name + ", ")
            #increment counter
            counter += 1

        #updating the date
        currDate += timedelta(days=1)
        day += 1


# Method the designs the GUI for this program
def CreateGUIFillNames(numOfPeople, numOfDays):
    # list of names
    listOfNames = []
    listOfEntries = []

    numOfPeople = int(numOfPeople)
    numOfDays = int(numOfDays)

    # Function that calls the RNG
    def CallRNG():
        for i in range(0, numOfPeople):
            #fetch an entry
            entry = listOfEntries[i]
            #retrieve the name
            listOfNames.append(entry.get())
        # Generate the list
        RNG(numOfPeople, numOfDays, listOfNames)
        # once done, notify the user
        masterFillNames.destroy()
        CreateGUISuccess()


    # function that goes back to the previous GUI
    def GoBack():
        masterFillNames.destroy()
        CreateGUIPrompt()

    # Window
    masterFillNames = tk.Tk()
    tk.Label(masterFillNames, text="Input the names").grid(row=0, column=0)

    for i in range(1, numOfPeople + 1):
        entry = tk.Entry(masterFillNames)
        entry.grid(row=i, column=0)
        listOfEntries.append(entry)

    tk.Button(masterFillNames, text='Create', command=CallRNG).grid(row=numOfPeople+2, column=0, sticky=tk.W)
    tk.Button(masterFillNames, text='Back', command=GoBack).grid(row=numOfPeople+2, column=1, sticky=tk.W)

    tk.mainloop()




# GUI function that prompts the user to enter the number of people and the number of days
# source: https://www.python-course.eu/tkinter_entry_widgets.php
def CreateGUIPrompt():

    def CallGUIFillNames():
        if e1.get().isdigit() and e2.get().isdigit():
            numOfPeople = e1.get()
            numOfDays = e2.get()
            masterPrompt.destroy()
            CreateGUIFillNames(numOfPeople, numOfDays)
        else:
            print("ERROR! ONE OF THE FIELDS IS EMPTY OR YOU DIDNT PASS A DIGIT")

    masterPrompt = tk.Tk()
    tk.Label(masterPrompt,
             text="Enter the number of people:").grid(row=0)
    tk.Label(masterPrompt,
             text="Enter the number of Days:").grid(row=1)

    e1 = tk.Entry(masterPrompt)
    e2 = tk.Entry(masterPrompt)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    tk.Button(masterPrompt, text='Create', command=CallGUIFillNames).grid(row=3, column=0, sticky=tk.W, pady=4)
    tk.mainloop()

# GUI that notifies the user
def CreateGUISuccess():
    masterSuccess = tk.Tk()
    tk.Label(masterSuccess, text="The sheet has been generated!").grid(row=0)
    tk.Button(masterSuccess, text="Quit", command=masterSuccess.destroy).grid(row=1)
    tk.mainloop()

if __name__ == '__main__':
    CreateGUIPrompt()