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
refCodes = { 
    '0' : [0, 0, 0, 1, 1, 0, 1],
    '1' : [0, 0, 1, 1, 0, 0, 1],
    '2' : [0, 0, 1, 0, 0, 1, 1],
    '3' : [0, 1, 1, 1, 1, 0, 1],
    '4' : [0, 1, 0, 0, 0, 1, 1],
    '5' : [0, 1, 1, 0, 0, 0, 1],
    '6' : [0, 1, 0, 1, 1, 1, 1],
    '7' : [0, 1, 1, 1, 0, 1, 1],
    '8' : [0, 1, 1, 0, 1, 1, 1],
    '9' : [0, 0, 0, 1, 0, 1, 1]
}
def getCode(lines):
    unitLength = lines[0][1]
    binaryCode = []
    for i, line in enumerate(lines):
        for count in range(int(line[1]/unitLength)):
            if (line[0] == 'B'):
                binaryCode.append(0)
            if (line[0] == 'W'):
                binaryCode.append(1)
    del binaryCode[0:3]; del binaryCode[42:47]; del binaryCode[-3:]
    pp.pprint(binaryCode)
    print(len(binaryCode))
    binaryCode = np.array_split(binaryCode, 2)
    leftParity = np.array_split(binaryCode[0], 6)
    rightParity = np.array_split(binaryCode[1], 6)
    pp.pprint(leftParity)
    pp.pprint(rightParity)
    decimalCode = []

    def inversion(x):
        def complement(n):
            if (n == 0): 
                return 1
            else: 
                return 0
        return list(map(complement, x))
     
    for refCode in leftParity:
        for key, value in refCodes.items():
            if (np.array_equal(refCode, inversion(value))):
                decimalCode.append(key)
                break

    for refCode in rightParity:
        for key, value in refCodes.items():
            if (np.array_equal(refCode, value)):
                decimalCode.append(key)
                break
    pp.pprint(decimalCode)
getCode(lineInfo)
plt.show()
