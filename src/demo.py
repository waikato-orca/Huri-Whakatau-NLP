import matplotlib.pyplot as plt
from math import sin, pi, cos

def getColor(title, user):
    colors = COLORS[:len(title)]
    for a_user, color in zip(title, colors):
        if a_user == user:
            return color


COLORS = ["red", "blue", "green", "purple", "black", "brown", "orange", "pink"]
f = open("results.csv", mode = "r")
title = f.readline()
title = title.split(',')
title = title[1:-1]
print(title)

polyptsB = []
fig = plt.figure(figsize = (4.7,4.7))
ax = fig.add_subplot(111)
ax.axis("off")
# plotPolygonPts(ax, fig, user, window)
x = []
y = []
n = len(title)
r = 0.5 / sin(pi/n)
angle = (2 * pi) / n
for i in range(n):
    xcoord = r * cos(i * angle)
    x.append(xcoord)
    ycoord = r * sin(i * angle)
    y.append(ycoord)
    polyptsB.append([xcoord, ycoord])
x.append(x[0])
y.append(y[0])
ax.plot(x, y, color = "black")
i = 0
for user in title:
    x1 = [x[i]]
    y1 = [y[i]]
    ax.scatter(x1, y1, color = getColor(title, user))
    i += 1
fig.canvas.draw()

i = 1
alpha = 1 / 106
line = f.readline()
while line != "":
    line = line.split(',')
    user = line[-1].split('\n')[0]
    line = line[1:-1]
    xcoord = 0
    ycoord = 0
    for para1, coord in zip(line, polyptsB):
        # print(str(para1) + " " + str(coord[0]))
        xcoord += float(para1) * coord[0]
        ycoord += float(para1) * coord[1]
    alpha1 = alpha * i

    ax.scatter([xcoord], [ycoord], color = "black", alpha=alpha1)
    fig.canvas.draw()
    line = f.readline()
    i += 1
    # print(line)
textObj = ax.text(0, 1, "make_your_bedA")
plt.show()