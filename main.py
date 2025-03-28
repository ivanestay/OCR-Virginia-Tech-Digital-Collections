import pytesseract
# Import Python-tesseract
from PIL import Image
import glob
# Try using opencv-python if cv2 does not work in the settings
import cv2 as cv
import json
import os
import numpy as np
from matplotlib import pyplot as plt

# Since the pytesseract file path is different due to Tesseract being a port to Windows,
# we have to note the new file path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ivanestay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# We retrieve these images from a folder using glob and then use an array to store them.
# We start with the "regular" files (the ones without any handwriting).
path = glob.glob("C:/Users/ivanestay/Downloads/BARTER_COLLECTION/regular/*.jpg")
#cv_img = []
#cv2_img = []
#cv3_img = []
for img in path:
    # Loads the image in grayscale.
    n = cv.imread(img,0)
    z = cv.medianBlur(n,3)
    # For these images, we need to apply the thresholding step.
    # In other words, we convert them from grayscale to just black and white.
    # Otherwise, different colored font would not be picked up.
    ret,th1 = cv.threshold(z,127,255,cv.THRESH_BINARY)
    #th2 = cv.adaptiveThreshold(z, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                             #cv.THRESH_BINARY, 7, 2)
    #th3 = cv.adaptiveThreshold(z,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            #cv.THRESH_BINARY,7,2)
    #blur = cv.GaussianBlur(n, (5, 5), 0)
    #ret3, th3 = cv.threshold(n, 100, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    #cv_img.append(th1)
    file_name = os.path.basename(img)
    file_name_no_extension = os.path.splitext(os.path.basename(img))[0]
    text = pytesseract.image_to_string(th1)
    data = {
        "image": file_name,
        "output": text
    }
    with open("C:/Users/ivanestay/Downloads/BARTER_COLLECTION/output/"+file_name_no_extension+".json", "w") as f:
        json.dump(data, f, indent=4)
    #cv2_img.append(th2)
    #cv3_img.append(th3)

# We now repeat with the files with handwriting
path2 = glob.glob("C:/Users/ivanestay/Downloads/BARTER_COLLECTION/handwriting/*.jpg")
for img in path2:
    n = cv.imread(img,0)
    z = cv.medianBlur(n,3)
    ret,th1 = cv.threshold(z,100,255,cv.THRESH_BINARY)
    #cv_img.append(th1)
    file_name = os.path.basename(img)
    file_name_no_extension = os.path.splitext(os.path.basename(img))[0]
    text = pytesseract.image_to_string(th1)
    data = {
        "image": file_name,
        "output": text
    }
    with open("C:/Users/ivanestay/Downloads/BARTER_COLLECTION/output/" + file_name_no_extension + ".json", "w") as f:
        json.dump(data, f, indent=4)

#img = cv.imread('C:/Users/ivanestay/Downloads/BARTER_COLLECTION/BTR_BTR_000001_0001.jpg',0)
#img = cv.medianBlur(img,5)
#ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)

# Below are alternate thresholding methods I used to determine which one would be the best
# th1 was ultimately the one I used, will store these for reference in case adjustments are necessary

#titles = ['Global Thresholding (v = 127)',
            #'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
#for i in range(len(cv_img)):
    #images = [cv_img[i], cv2_img[i], cv3_img[i]]
    #for j in range(3):
        #plt.subplot(2,2,j+1),plt.imshow(images[j],'gray')
        #plt.title(titles[j])
        #plt.xticks([]),plt.yticks([])
    #plt.show()"

# Iterates through the array and prints the output, will be stored in a csv file later on
#for n in range(len(cv_img)):
    #text = pytesseract.image_to_string(cv_img[n])
    #outputfile = "C:/Users/ivanestay/Downloads/BARTER_COLLECTION/output/output_"+str(n)+".txt"
    #f = open(outputfile, "w")
    #f.writelines("VIRGINIA TECH DIGITAL COLLECTIONS. DATA STARTS ON NEXT ROW: \n")
    #f.writelines(text)
    #print(text)
    #f.close()
