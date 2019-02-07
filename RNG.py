import random
import time


def RNG(numOfPeople, numOfDays):
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

    #return the order
    return history

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


if __name__ == '__main__':
    print(RNG(3,6))