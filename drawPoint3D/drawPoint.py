import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def drawOutline(listx, listy, listz):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title("3D Curve")
    ax.plot(listx, listy, listz)
    plt.plot(listx, listy)
    plt.show()

x = []
y = []
z = []
fileX = open("F:/OutXList.txt")
fileY = open("F:/OutYList.txt")
indexX = 0
indexY = 0
indexZ = 1
while 1:
    lineX = fileX.readline()
    lineY = fileY.readline()
    if not lineX:
        break
    if not lineY:
        break
    xNumbers = lineX.split()
    yNumbers = lineY.split()
    for i in range(len(xNumbers)):
        x.insert(indexX, float(xNumbers[i]))
        y.insert(indexY, float(yNumbers[i]))
        z.insert(indexZ, float(indexZ))
    indexX += 1
    indexY += 1
    indexZ += 1
drawOutline(x, y, z)
fileX.close()
fileY.close()