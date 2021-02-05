from matplotlib import pyplot as plt
from matplotlib import image as pltImg
import numpy as np
import pprint as pp

def toBinaryImage(data, h, w):
    for i in range(h):
        for j in range(w):
            pix = data[i][j]
            if (pix[0]/3 + pix[1]/3 + pix[2]/3 >= 127.5):
                data[i][j] = [255, 255, 255]
            else:
                data[i][j] = [0, 0, 0]
 
original = pltImg.imread('barImgs/bar1.jpg') # Original Image(as a numPy N-D array) which we can't overwrite
#plt.figure(1); plt.imshow(original) # Plot it in a graph

data = original.copy() # Writable copy of our Image

height, width, mode = data.shape # Get the width height and mode(RGB-->3-D numPy array) of our Image

toBinaryImage(data, height, width) # Convert it purely to black and white, depending on its darkness
print(width)
# Assuming that our matrix is in perfect 2D shape and ready for horizontal scan, we do the following steps
B = [0, 0, 0]; W = [255, 255, 255]; MAX_DIVS = width
rowToScan = 125 
lineInfo = []
underScan = W 
plt.figure(2)
for i in range(width):
    BorW = data[rowToScan][i]
    if (BorW[0] != underScan[0]):
        if (BorW[0] == B[0]):
            lineInfo.append(['B', i - 1])
        if (BorW[0] == W[0]):
            lineInfo.append(['W', i - 1])
        plt.plot([i - 1, i - 1], [0, height])
        underScan = BorW

pp.pprint(lineInfo)
plt.imshow(data)
plt.show()