import numpy as np

topics = ["sweet_vs_savouryP", "pineapple_on_pizzaP", "ketchup_vs_mustardP","children_devicesP","pineapple_on_pizzaC","ketchup_vs_mustardC","children_devicesC","aiC","ketchup_vs_mustardB","children_devicesB","aiB", "children_devicesA", "aiA", "ketchup_vs_mustardA", "Mock Discussion", "welfareA", "pineapple_on_pizzaA"]

def getScore(line, f, f2):
    data = f.readline()
    users1 = []
    users2 = []
    while data != "" and data.split(',')[0] not in topics:
        users1.append(data.split(',')[0])
        # print(data)
        users2.append(data.split(',')[1].split("\n")[0])
        data = f.readline()
    jump = []
    for user1, user2 in zip(users1, users2):
        if user1 == user2:
            jump.append(0)
        else:
            jump.append(abs(users1.index(user1) - users2.index(user1)))
    count = 0
    max = 0
    total = 0
    for value in jump:
        total += value
        if value == 0:
            count += 1
        if value >= max:
            max = value
    f2.write(str(total) + "," + str(count) + "," + str(max) + "\n")
    i = len(users1) - 1
    # worstScore = 0
    # while i != 1:
    #     worstScore += (2 * i)
    #     if i < 2:
    #         i = 1
    #     else:
    #         i -= 2
    return data

f = open("pairwise.csv", mode = "r")
f2 = open("score.csv", mode = "a")
line = f.readline()
topic = line.split(',')[0]
f2.write(topic + "\n")
while line.split(',')[0] in topics:
    line = getScore(line, f, f2)
    topic = line.split(',')[0]
    f2.write(topic + "\n")
print("Done")