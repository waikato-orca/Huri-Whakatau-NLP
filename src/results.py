import numpy as np

def processDiscussion(line, f):
    users = line[1:-1]
    data = f.readline()
    rows = []
    processed = []
    while data != "" and data.split(',')[0] != "children_devicesA":
        rows.append(data)
        data = f.readline()
    for row in rows:
        row = row.split(',')
        row.insert(0, row[-1])
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
        matrix = matrix[1:]
        i = 0
        j = 0
        total = 0
        for j in range(len(matrix[0])):
            for i in range(len(matrix)):
                total += matrix[i][j]
            total /= len(matrix)
            average.append(total)
        finalResult.append(average)
    print(finalResult)
    return

f = open("results.csv", mode = "r")
line = f.readline()
line = line.split(',')
if line[0] == "children_devicesA":
    processDiscussion(line, f)