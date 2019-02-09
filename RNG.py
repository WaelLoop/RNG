import random
import time
from datetime import datetime,timedelta

def RNG(numOfPeople, numOfDays):

    #list of names
    listOfNames = []

    for numbers in range(1,numOfPeople+1):
        name = input("Input the names: ")
        listOfNames.append(str(name))

    # empty list of RNG
    randomized = []

    # our cumalitve number of times someone was assigned
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


if __name__ == '__main__':
    people = input("Enter the number of people: ")
    days = input("Enter the number of days: ")
    RNG(people,days)