topics = ["sweet_vs_savouryP", "pineapple_on_pizzaP", "ketchup_vs_mustardP","children_devicesP","pineapple_on_pizzaC","ketchup_vs_mustardC","children_devicesC","aiC","ketchup_vs_mustardB","children_devicesB","aiB", "children_devicesA", "aiA", "ketchup_vs_mustardA", "Mock Discussion", "welfareA", "pineapple_on_pizzaA"]

def getProbability(line, f, f2):
    users = line.split(',')[1:-1]
    data = f.readline()
    ranking = {}
    count = 0
    for user in users:
        if user not in ranking:
            ranking[user] = {}
            for i in range(len(users)):
                ranking[user][i + 1] = 0
    while data != "" and data.split(',')[0] not in topics:
        data = data.split(',')[:-1]
        for i in range(len(data)):
            ranking[data[i]][i + 1] += 1
        data = f.readline()
        count += 1
    for i in range(len(users)):
        f2.write(str(i + 1) + ",")
        for user in ranking:
            dict = ranking[user]
            f2.write(str((dict[i + 1])/count) + ",")
            dict[i + 1] = dict[i + 1]/count
        f2.write("\n")
    f2.write("Mean,")
    meanArray = []
    for user in ranking:
        mean = 0
        dict = ranking[user]
        for rank in dict:
            mean += rank * dict[rank]
        f2.write(str(mean) + ",")
        meanArray.append(mean)
    f2.write("\n")
    f2.write("Std Dev,")
    index = 0
    for user in ranking:
        stdev = 0
        dict = ranking[user]
        for rank in dict:
            stdev += ((rank - meanArray[index]) ** 2) * dict[rank]
        stdev **= 0.5
        f2.write(str(stdev) + ",")
        index += 1
    f2.write("\n")
    return data

f = open("ranking.csv", mode = "r")
f2 = open("probability.csv", mode = "a")
line = f.readline()
topic = line.split(',')[0]
f2.write(line)
while line.split(',')[0] in topics:
    line = getProbability(line, f, f2)
    f2.write(line)
    topic = line.split(',')[0]
print("Done")