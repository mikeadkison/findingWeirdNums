import copy
import time
def fact(n):
    if n == 0:
        return 1
    z = 1
    i = 1
    while i < n:
        i += 1
        z = z * i
    return float(z)

def C(n,r):
    if r > n:
        return 0
    z = fact(n) / (fact(r) * (fact(n-r)))
    return float(z)

##############################
##############################
######P(n,n) stuff############
##############################

def permutations(elements):
    ##BASE CASE
    if len(elements) == 1:
        listOfList = [elements]
        return listOfList;
    ##RECURSION
    perms = []
    for element in elements:
        shallowElementsCopy = elements[:]
        shallowElementsCopy.remove(element)
        subProblemPermutations = permutations(shallowElementsCopy)
        for permutation in subProblemPermutations:
            permutation.insert(0, element)
            perms.append(permutation)
    return perms
#########################end##
##############################
def outputPermutations(m, k): #Number of objects, number of objects to select
    #Finding all outcomes with replacement, but picking out the permutations
    Combs = []
    Outcome = [] 
    for i in range(int(k)):
        Outcome.append(1)
        
    while len(Combs) < C(m, k):
        startTime = time.time()
        #Checks to see if the outcome has unique numbers for distinguished case
        c_check = []
        for i in range(1, int(m)+1):
            c_check.append(Outcome.count(i))
        if max(c_check) == 1:
            y = copy.deepcopy(Outcome)
            Combs.append(y)
            
        #Finds next output
        if Outcome[-1] < m:
            Outcome[-1] = Outcome[-1] + 1
                            
        elif Outcome[-1] == m:
            target_place = Outcome.index(m)
            Outcome[target_place-1] = Outcome[target_place-1] + 1
            for i in range(target_place, int(k)):
                Outcome[i] = Outcome[target_place-1]

    endTime = time.time() - startTime
    #print endTime
    return [permutation for comb in Combs for permutation in permutations(comb)]
    


def getDigit(num, digit):
    numLength = getLength(num)
    if (digit > numLength - 1) or (digit < 0):
        return -1
    if (digit == 0):
        divider = 1
        remainder = -1
        for i in range(0, numLength):
            remainder = num % 10
            num = num / 10
        return remainder

    remainder = -1
    for i in range(0, numLength - digit):
        remainder = num % 10
        num /= 10
    return remainder



def getLength(num):
    length = 1
    multiplier = 10
    while num / multiplier > 0:
        length = length + 1
        multiplier = multiplier * 10

    return length

def removeDigit(num, digitIndex):
    digitIndexToRemove = digitIndex
    newNum = 0
    multiplier = 1
    currentDigitIndex = getLength(num) - 1
    while currentDigitIndex >= 0:
        if currentDigitIndex != digitIndexToRemove:
            newNum = newNum + getDigit(num, currentDigitIndex)  * multiplier
            multiplier = multiplier * 10
        currentDigitIndex = currentDigitIndex - 1
    return newNum

for firstNum in range(10, 1000):
    for secondNum in range(10, 1000):
        if (firstNum != secondNum):
            actualAnswer = float(firstNum) / secondNum
            for k in range(1, getLength(firstNum)):
                permutes = outputPermutations(getLength(firstNum), k) #size of num P k
                #print permutes
                for firstPerm in permutes:
                    for secondPerm in permutes:
                        firstPermDigits = []
                        secondPermDigits = []
                        for i in range(0, len(firstPerm)):
                            firstPermDigits = firstPermDigits + [getDigit(firstNum, firstPerm[i] - 1)]
                            secondPermDigits = secondPermDigits + [getDigit(secondNum, secondPerm[i] - 1)]
                        if firstPermDigits == secondPermDigits: #digits cancel with each other
                            #print firstNum, secondNum
                            #remove digits and see if it works
                            firstNumLess = firstNum
                            for i in range(0, len(firstPerm)):
                                firstNumLess = removeDigit(firstNumLess, firstPerm[i] - 1)
                                for k in range(i + 1, len(firstPerm)):
                                    if firstPerm[i] < firstPerm[k]:
                                        firstPerm[k] = firstPerm[k] - 1

                            secondNumLess = secondNum
                            for i in range(0, len(secondPerm)):
                                secondNumLess = removeDigit(secondNumLess, secondPerm[i] - 1)
                                for k in range(i + 1, len(secondPerm)):
                                    if secondPerm[i] < secondPerm[k]:
                                        secondPerm[k] = secondPerm[k] - 1
                            if (firstNumLess != firstNum / 10 or secondNumLess != secondNum / 10):
                                if secondNumLess != 0: #division by 0
                                    if abs(float(firstNumLess) / secondNumLess - actualAnswer) < 0.00001: #approximate error
                                        print firstNum, secondNum, firstNumLess, secondNumLess, firstPermDigits, secondPermDigits, actualAnswer