from matplotlib import pyplot as plt
from matplotlib import image as pltImg
import numpy as np
import pprint as pp

refCodes = { # Barcode language(for reading from right end to center)
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

B = [0, 0, 0] # Black
W = [255, 255, 255] # White

def toBinaryImage(data, h, w):
    for i in range(h):
        for j in range(w):
            pix = data[i][j]
            if (pix[0]/3 + pix[1]/3 + pix[2]/3 >= 127.5):
                data[i][j] = [255, 255, 255]
            else:
                data[i][j] = [0, 0, 0]
    return data

def getWidthOfStripes(lineInfo):
    for i in range(len(lineInfo) - 1): 
            lineInfo[i][1] = lineInfo[i + 1][1]  - lineInfo[i][1]
    lineInfo.pop()
    print("\nData with length of each stripe")
    pp.pprint(lineInfo)

def printNoOfStripes(lineInfo):
    sum = 0
    for line in lineInfo:
        sum += line[1]
    unitLineLength = lineInfo[0][1]
    totalStripes = sum/unitLineLength
    print("\nWidth of scan area: " + str(sum) + "\n", "\bTotal Stripes: " + str(totalStripes))
    
def getLineInfo(imgPath, rowToScan): 
    # SETUP   
    ORIGINAL = pltImg.imread(imgPath) 
    height, width, mode = ORIGINAL.shape
    OurCopy = ORIGINAL.copy() 
    lineInfo = []

    # Create plot for image
    plt.subplot(1, 2, 1)
    plt.title("Working Image")

    if (mode == 3):
        # Change our image into B and W
        Data = toBinaryImage(OurCopy, height, width) 
        underScan = W 
    
        # Record the indices of change in colour(stripes) and put it inside the array lineInfo
        for i in range(width):
            BorW = Data[rowToScan][i]
            if (BorW[0] != underScan[0]):
                if (BorW[0] == B[0]):
                    lineInfo.append(['B', i])
                if (BorW[0] == W[0]):
                    lineInfo.append(['W', i])
                plt.plot([i, i], [0, height], linewidth = 1)
                underScan = BorW

        print("Data with index(coloumns)"); pp.pprint(lineInfo)

        # Few function calls
        getWidthOfStripes(lineInfo)
        printNoOfStripes(lineInfo)

        # Plotting
        plt.imshow(Data)
        plt.subplot(1, 2, 2)
        plt.title("Original")
        plt.imshow(ORIGINAL)
    else: 
        print("Image mode incompatible") 

    return lineInfo

def getBinaryCode(Stripes):
    unitLength = Stripes[0][1]
    binaryCode = []
    for i, line in enumerate(Stripes):
        for count in range(int(line[1]/unitLength)):
            if (line[0] == 'B'):
                binaryCode.append(0)
            if (line[0] == 'W'):
                binaryCode.append(1)

    del binaryCode[0:3]; del binaryCode[42:47]; del binaryCode[-3:]

    print("Stripes under scan: " + str(len(binaryCode)))
    print("Binary Code of our barcode: " + str(binaryCode))
    binaryCode = np.array_split(binaryCode, 2)
    
    return binaryCode

def invertBits(arrayOfOnesAndZeroes):
    def complement(n):
        if (n == 0): 
            return 1
        else: 
            return 0
    return list(map(complement, arrayOfOnesAndZeroes))

def getCode(Stripes):
    binaryCode = getBinaryCode(Stripes)

    leftParity = np.array_split(binaryCode[0], 6); 
    rightParity = np.array_split(binaryCode[1], 6)

    CodeArray = []

    for refCode in leftParity:
        for key, value in refCodes.items():
            if (np.array_equal(refCode, invertBits(value))):
                CodeArray.append(key)
                break

    for refCode in rightParity:
        for key, value in refCodes.items():
            if (np.array_equal(refCode, value)):
                CodeArray.append(key)
                break
    
    print("Code Array: " + str(CodeArray))

lineInfo = getLineInfo('barImgs/bar6.jpg', 75)

getCode(lineInfo)

plt.show()