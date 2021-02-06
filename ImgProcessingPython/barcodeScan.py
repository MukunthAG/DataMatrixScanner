from matplotlib import lines, pyplot as plt
from matplotlib import image as pltImg
import numpy as np
import pprint as pp

def getLineInfo(imgPath, rowToScan):
    def toBinaryImage(data, h, w):
        for i in range(h):
            for j in range(w):
                pix = data[i][j]
                if (pix[0]/3 + pix[1]/3 + pix[2]/3 >= 127.5):
                    data[i][j] = [255, 255, 255]
                else:
                    data[i][j] = [0, 0, 0]
    
    ORIGINAL = pltImg.imread(imgPath) 
    data = ORIGINAL.copy() 
    height, width, mode = data.shape
    lineInfo = []
    if (mode == 3):
        toBinaryImage(data, height, width) 
        B = [0, 0, 0] 
        W = [255, 255, 255]
        underScan = W 
        #plt.figure(1)
        plt.subplot(1, 2, 1)
        plt.title("Working Image")
        for i in range(width):
            BorW = data[rowToScan][i]
            if (BorW[0] != underScan[0]):
                if (BorW[0] == B[0]):
                    lineInfo.append(['B', i])
                if (BorW[0] == W[0]):
                    lineInfo.append(['W', i])
                plt.plot([i, i], [0, height], linewidth = 1)
                underScan = BorW

        print("Data with index(coloumns)")
        pp.pprint(lineInfo)
        for i in range(len(lineInfo) - 1): 
            lineInfo[i][1] = lineInfo[i + 1][1]  - lineInfo[i][1]

        lineInfo.pop()
        print("Data with length of each stripe")
        pp.pprint(lineInfo)

        sum = 0
        for line in lineInfo:
            sum += line[1]
        
        unitLineLength = lineInfo[0][1]
        print(sum, sum/unitLineLength)
        plt.imshow(data)
        plt.subplot(1, 2, 2)
        plt.title("Original")
        plt.imshow(ORIGINAL)
    else: 
        print("Image mode incompatible") 

    return lineInfo
    

lineInfo = getLineInfo('barImgs/bar6.jpg', 75)

plt.show()