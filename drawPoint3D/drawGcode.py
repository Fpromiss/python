import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def draw_out_line(list_x, list_y, list_z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_title("3D Curve")
    ax.plot(list_x, list_y, list_z)
    plt.plot(list_x, list_y)
    plt.show()


if __name__ == '__main__':
    # ������x�߽����� y�߽����� z�߽�����
    x = []
    y = []
    z = []
    # ��ȡGCode����
    gCodeData = open("F:/outGcode.txt")
    # �����Ӧ�߽����ݲ��±�
    indexX = 0
    indexY = 0
    indexZ = 0
    # ���嵱ǰ���
    nowFloorHeight = 1
    while 1:
        # ��ȡÿһ��GCode
        lineGCodeFData = gCodeData.readline()
        # �����ȡ��� ����ѭ��
        if not lineGCodeFData:
            break
        # �ָ�ÿһ��GCode
        dataNumbers = lineGCodeFData.split()
        # ��ÿһ�н����ж�
        for i in range(len(dataNumbers)):
            if dataNumbers[0] == "G1":
                if len(dataNumbers) >= 4:
                    if dataNumbers[3][0] == 'F':
                        nowFloorHeight += 1
                        break
                    if dataNumbers[1][0] == "X" and dataNumbers[2][0] == "Y" and dataNumbers[3][0] == "E":
                        x.insert(indexX, float(dataNumbers[1][1:]))
                        y.insert(indexY, float(dataNumbers[2][1:]))
                        z.insert(indexZ, float(nowFloorHeight))
        if nowFloorHeight == 10:
            print(dataNumbers)
        indexX += 1
        indexY += 1
        indexZ += 1
    draw_out_line(x, y, z)
    gCodeData.close()
