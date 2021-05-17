import numpy as np

topics = ["sweet_vs_savouryP", "pineapple_on_pizzaP", "ketchup_vs_mustardP","children_devicesP","pineapple_on_pizzaC","ketchup_vs_mustardC","children_devicesC","aiC","ketchup_vs_mustardB","children_devicesB","aiB", "children_devicesA", "aiA", "ketchup_vs_mustardA", "Mock Discussion", "welfareA", "pineapple_on_pizzaA"]

def processDiscussion(line, f, f2):
    users = line.split(',')[1:-1]
    data = f.readline()
    rows = []
    processed = []
    while data != "" and data.split(',')[0] not in topics:
        rows.append(data)
        data = f.readline()
    for row in rows:
        row = row.split(',')
        row.insert(users.index(row[-1].split("\n")[0]) + 1, 0)
        row.insert(0, row[-1].split("\n")[0])
        row.pop(-1)
        processed.append(row)
    userSpecific = {}
    for row in processed:
        if row[0] not in userSpecific:
            userSpecific[row[0]] = {}
            userSpecific[row[0]][row[1]] = row[2:]
        else:
            userSpecific[row[0]][row[1]] = row[2:]
    finalResult = []
    superFinalResult = []
    for user in userSpecific:
        matrix = []
        average = []
        prev = np.zeros(len(users))
        for index in userSpecific[user]:
            curr = userSpecific[user][index]
            temp = []
            for para in curr:
                newPara = float(para)
                temp.append(newPara)
            curr = []
            for prev1, temp1 in zip(prev, temp):
                curr.append(temp1 - prev1)
            matrix.append(curr)
            prev = temp
        matrix = matrix[1:]
        i = 0
        j = 0
        if len(matrix) > 0:
            for j in range(len(matrix[0])):
                total = 0
                for i in range(len(matrix)):
                    total += matrix[i][j]
                # total /= len(matrix)
                average.append(total)
            finalResult.append(average)
        else: finalResult.append(np.zeros(len(users)))
    i = 0
    j = 0
    string = "self exclusive,"
    for j in range(len(finalResult[0])):
        total = 0
        for i in range(len(finalResult)):
            total += finalResult[i][j]
        superFinalResult.append(abs(total))
        string += str(abs(total)) + ","
    string += "\n"
    f2.write(string)
    return data

f = open("results.csv", mode = "r")
f2 = open("ringleader.csv", mode = "a")
line = f.readline()
f2.write(line)
topic = line.split(',')[0]
while line.split(',')[0] in topics:
    line = processDiscussion(line, f, f2)
    if line.split(',')[0] != topic:
        f2.write(line)
        topic = line.split(',')[0]
print("Done")