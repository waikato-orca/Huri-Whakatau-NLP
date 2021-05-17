topics = ["sweet_vs_savouryP", "pineapple_on_pizzaP", "ketchup_vs_mustardP","children_devicesP","pineapple_on_pizzaC","ketchup_vs_mustardC","children_devicesC","aiC","ketchup_vs_mustardB","children_devicesB","aiB", "children_devicesA", "aiA", "ketchup_vs_mustardA", "Mock Discussion", "welfareA", "pineapple_on_pizzaA"]

def getRankings(line, f, f2):
    users = line.split(',')[1:-1]
    data = f.readline()
    while data != "" and data.split(',')[0] not in topics:
        data = data.split(',')[1:-1]
        floatData = []
        for rank in data:
            floatData.append(float(rank))
        sort = sorted(floatData, reverse=1)
        for rank in sort:
            f2.write(users[floatData.index(rank)] + ",")
        f2.write("\n")
        data = f.readline()
    return data

f = open("ringleader.csv", mode = "r")
f2 = open("ranking.csv", mode = "a")
line = f.readline()
topic = line.split(',')[0]
f2.write(line)
while line.split(',')[0] in topics:
    line = getRankings(line, f, f2)
    f2.write(line)
    topic = line.split(',')[0]
print("Done")