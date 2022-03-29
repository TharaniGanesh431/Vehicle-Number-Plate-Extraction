import cv2
import numpy as np
import math
import os

k = cv2.ml.KNearest_create()

def loadAndTrainML():
    allContoursWithData = []              
    validContoursWithData = []             

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)               
    except:                                                                              
        print("error, unable to open classifications.txt, exiting program\n")            
        os.system("pause")
        return False                                                                       

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                
    except:                                                                                
        print("error, unable to open flattened_images.txt, exiting program\n")             
        os.system("pause")
        return False                                                                       

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       

    k.setDefaultK(1)                                                           

    k.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)         

    return True

def recognizeChar(threshold, contour):
    Chars = ""

    contour.sort(key = lambda matchingChar: matchingChar.CenterX)        

    for c in contour:

        imgROI = threshold[c.Y : c.Y + c.Height,
                           c.X : c.X + c.Width]

        imgROIResized = cv2.resize(imgROI, (20, 30))          

        npaROIResized = imgROIResized.reshape((1, 20 * 30))      

        npaROIResized = np.float32(npaROIResized)               

        retval, npaResults, neigh_resp, dists = k.findNearest(npaROIResized, k = 1)

        Chars = Chars + str(chr(int(npaResults[0][0])))                  


    return Chars


