from matplotlib import pyplot as plt
from matplotlib import image as pltImg
import numpy as np

def toBinaryImage(data, w, h):
    for i in range(w):
        for j in range(h):
            pix = data[i][j]
            if (pix[0]/3 + pix[1]/3 + pix[2]/3 >= 127.5):
                data[i][j] = [255, 255, 255]
            else:
                data[i][j] = [0, 0, 0]
 
original = pltImg.imread('barImgs/bar1.jpg') # Original Image(as an numPy N-D array) which we can't overwrite

data = original.copy() # Writable copy of our Image

width, height, mode = data.shape # Get the width height and mode(RGB-->3) of our Image

toBinaryImage(data, width, height) # Convert it purely to black and white, depending on its darkness

plt.figure(1); plt.imshow(original)
plt.figure(2); plt.imshow(data)
plt.show()