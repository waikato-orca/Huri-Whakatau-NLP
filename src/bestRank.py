import numpy as np

topics = ["sweet_vs_savouryP", "pineapple_on_pizzaP", "ketchup_vs_mustardP","children_devicesP","pineapple_on_pizzaC","ketchup_vs_mustardC","children_devicesC","aiC","ketchup_vs_mustardB","children_devicesB","aiB", "children_devicesA", "aiA", "ketchup_vs_mustardA", "Mock Discussion", "welfareA", "pineapple_on_pizzaA"]

def getBestRank(line, f, f2):
    users = line.split(',')[1:-1]
    data = f.readline()
    while data.split(',')[0] != "Mean":
        data = f.readline()
    meanArray = data.split(',')[1:-1]
    data = f.readline()
    stdevArray = data.split(',')[1:-1]
    sortedMeanArrayInd = np.argsort(meanArray)
    sortedstdArray = np.array(stdevArray)[sortedMeanArrayInd]
    sortedMeanArray = np.array(meanArray)[sortedMeanArrayInd]
    sortedUser = np.array(users)[sortedMeanArrayInd]
    for i in range(len(sortedMeanArray)-1):
        if sortedMeanArray[i] == sortedMeanArray[i+1]:
            if sortedstdArray[i] > sortedstdArray[i+1]:
                temp = sortedUser[i]
                sortedUser[i] = sortedUser[i+1]
                sortedUser[i+1] = temp 
    for user in sortedUser:
        f2.write(user + "\n")
    data = f.readline()
    return data

f = open("probability.csv", mode = "r")
f2 = open("bestRank.csv", mode = "a")
line = f.readline()
topic = line.split(',')[0]
f2.write(topic + "\n")
while line.split(',')[0] in topics:
    line = getBestRank(line, f, f2)
    topic = line.split(',')[0]
    f2.write(topic + "\n")
print("Done")